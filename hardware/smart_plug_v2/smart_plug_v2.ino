#include <WiFiManager.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>

#include "ACS712.h"
#include "time.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// ESP32 Pins
#define CUR_SENSOR A3                 // adjust pins as necessary
#define VOLT_SENSOR A2
#define RELAY 15

// Constants
#define WALL_FREQ 60                  // US = 60hz
#define WALL_VOLT 120                 // US = 120 V
#define DELAY_MS 1000                 // adjust this to change data transmit rate
#define MAX_RETRY 30                  // adjust this to determine how many times ESP32 tries to connect to network
#define MAX_MSG 30                    // adjust this to determine max MQTT message length
#define MAC_ADDR_LEN 17               // length of MAC address in characters (includes colons)
#define MAX_TIME_LEN 20               // length of string-formatted 

// Running average
#define DATA_BUFFER 4096
#define DATA_COUNT 20
int count=0;                          // track number of data points summed 
float average = 0, running_total=0;   // total sum of data for averaging

// Timestamps
// source: https://randomnerdtutorials.com/epoch-unix-time-esp32-arduino/
const char* ntpServer = "pool.ntp.org";
unsigned long epochTime; 
char displayTime[MAX_TIME_LEN];

// Network
String ssid         = "iPhone";                                     // SSID of network to be connected to
String password     = "yaaabruh";                                   // password of network to be connected to

// MQTT
String mqttDataTopic    = "plux/data/";                             // publishing topic for plug, will be cominbed with MAC address later
String mqttCtrlTopic    = "plux/control/";                          // subscribing topic for plug, will be cominbed with MAC address later
String mqttServer       = "mosquitto.projectplux.info";
const int   mqttPort         = 1883;                                // 1883 = insecure port, 8883 = secure port (via TLS)
String mqttUser         = "eric";
String mqttPassword     = "truong";

// Static variables
static char mqtt_msg[MAX_TIME_LEN + MAX_MSG];                                           // buffer for MQTT message (timestamp + power)
static char mac_addr[MAC_ADDR_LEN];                                                     // buffer for MAC address (48 bits/8 = 6 bytes);
String mqttDataTopicStr;                                    // buffer for data topic name
String mqttCtrlTopicStr;                                    // buffer for ctrl topic name

// Object constructors
ACS712  ACS(A2, 5.0, 4095, 66);      // call ACS712.h constructor for 30A variant
WiFiClient espClient;                // call WiFi constructor
PubSubClient client(espClient);      // call MQTT constructor
WiFiManager wm;                      // call WiFi manager constructor (source: https://dronebotworkshop.com/wifimanager/)

// Function declarations - General
static void printLocalTime();

// Function declarations - MQTT
static int mqtt_setup();
static void msg_receive(char *topic, byte* payload, unsigned int length);

/* initialization function for ESP32
 * sources: https://github.com/RobTillaart/ACS712/blob/master/examples/ACS712_20_AC/ACS712_20_AC.ino
 *          https://dronebotworkshop.com/wifimanager/
 */
void setup() { 
  Serial.begin(115200);                                       // set up baud rate for debugging
  pinMode(CUR_SENSOR, INPUT);                                 // set CUR_SENSOR to input mode
  pinMode(RELAY, OUTPUT);                                     // set RELAY pin to output mode
  Serial.println(__FILE__);

  //wm.resetSettings();                                           // comment this out when not testing (reminder: IP is 192.168.4.1)
  bool res = wm.autoConnect("PLUX", "12345678");                // use WiFi manager to dynamically add SSID/password
  if (!res) {
    Serial.println("setup(): connection failed");
    return;
  } else {
    Serial.println("setup(): connection successful");
  }
  
  int ret = mqtt_setup();                                         // attempt MQTT server connection
  if (ret) {
    Serial.println("setup(): unable to connect to MQTT server");
    return;
  } else {
    Serial.print("setup(): publishing to ");
    Serial.println(mqttDataTopicStr);
  }

  ret = client.subscribe(mqttCtrlTopicStr.c_str(), 0);                // subscribe to MQTT control topic
  if (!ret) {
    Serial.println("setup(): unable to subscribe to MQTT server topic");
    return;
  } else {
    Serial.print("setup(): subscribed to ");
    Serial.println(mqttCtrlTopicStr);
  }

  configTime(-28800, 3600, ntpServer);                        // configure time format for display
                                                              // -28800: UTC-8
                                                              // 3600: DST offset

  ACS.autoMidPoint(1);                                        // change this value to refine accuracy
}

/* main function for power monitoring and data transmission/reception
 * sources: https://randomnerdtutorials.com/esp32-mqtt-publish-subscribe-arduino-ide/
 */ 
void loop() {
  float mA = ACS.mA_AC(WALL_FREQ);                                // measure AC current
  float watts = (WALL_VOLT * mA) / 1000;                        // calculate power
  client.loop();                                                // keep listening on MQTT topic


//  Serial.print("Data: ");
//  Serial.print(mA);
//  Serial.print(" | Running total:");
//  Serial.print(running_total);
//  Serial.print(" | Count:");
//  Serial.println(count);
  int r = running_average(mA);
  if (r>0){
    mA = average;
//    Serial.print("Average: ");
//    Serial.println(average);
    printLocalTime();                                             // get timestamp and place in local buffer
    sprintf(mqtt_msg, "%s, %f", displayTime, mA);                 // convert number to string in string buffer
    memset(displayTime, '\0', MAX_TIME_LEN);                      // reset time buffer
    
    int ret = client.publish(mqttDataTopicStr.c_str(), mqtt_msg, false);  // send power data as string to MQTT data topic
    if (!ret) {
      Serial.println("loop(): unable to publish MQTT message");          
    } else {
      Serial.print("Data: ");
      Serial.print(mA);
      Serial.println(" | loop(): MQTT message published");
    }
    memset(mqtt_msg, '\0', MAX_MSG);                              // reset static buffer
  }
  delay(DELAY_MS);
}

/* helper function that gets current epoch time
 * sources: https://lastminuteengineers.com/esp32-ntp-server-date-time-tutorial/
 *          https://forum.arduino.cc/t/time-library-functions-with-esp32-core/515397/4
 */
static void printLocalTime(){
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
//    Serial.println("Failed to obtain time");
    return;
  }
//  Serial.print("printLocaltime(): ");
//  Serial.println(&timeinfo, "%Y-%m-%d %H:%M:%S");
  strftime(displayTime, MAX_TIME_LEN, "%Y-%m-%d %H:%M:%S", &timeinfo);
}

/* initialization of MQTT connection
 *  
 */
static int mqtt_setup() {
  client.setServer(mqttServer.c_str(), mqttPort);                         // set destination server
  while (!client.connected()) {
    Serial.println("mqtt_setup(): Connecting to MQTT...");
    if (client.connect("", mqttUser.c_str(), mqttPassword.c_str())) {
      Serial.println("mqtt_setup(): client connected");
    } else {
      Serial.print("mqtt_setup(): failed with state ");           // error message, print out failure state
      Serial.println(client.state());
      delay(1000);
    }
  }
  client.setCallback(msg_receive);                                // set callback function for receiving messages
  
  //sprintf(mqttDataTopicStr, "%s%s", mqttDataTopic, mac_addr);     // print concatenated string to data topic buffer
  //sprintf(mqttCtrlTopicStr, "%s%s",  mqttCtrlTopic, mac_addr);    // print concatenated string to control topic buffer
  mqttDataTopicStr = mqttDataTopic + WiFi.macAddress();
  mqttCtrlTopicStr = mqttCtrlTopic + WiFi.macAddress();
  
  Serial.println("mqtt_stetup(): complete");
  return 0;
}

/* helper callback function for receiving messages from server
 * sources: https://pubsubclient.knolleary.net/api#callback
 *          http://www.iotsharing.com/2017/08/how-to-use-esp32-mqtts-with-mqtts-mosquitto-broker-tls-ssl.html
 */
static void msg_receive(char *topic, byte* payload, unsigned int length) {

  // print topic
  Serial.print("msg_receive(): incoming message on ");
  Serial.println(topic);
  
  // de-encapsulate payload
  int msg = *payload;
  Serial.print("msg_receive(): payload - ");
  Serial.println(msg);
  switch (msg) {
    case 49: // turning ON circuit (ASCII 1 == int 49)
      digitalWrite(RELAY, HIGH);
      return;
    case 50: // turning OFF circuit (ASCII 2 == 50)
      digitalWrite(RELAY, LOW);
      return;
  }
}

static int running_average(float data){
  running_total+=data;
  count++;
  if (count>=DATA_COUNT){
    // do average and reset average,count
    average = running_total/DATA_COUNT;
    running_total = 0;
    count=0;
    return 1;
  }
  return 0;
}
