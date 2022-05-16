#include <ZMPT101B.h>
#include <WiFiManager.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>

#include "ACS712.h"
#include "time.h"

// ESP32 Pins
#define CUR_SENSOR A2                 // adjust pins as necessary
#define VOLT_SENSOR A3
#define RELAY 15

// Constants
#define WALL_FREQ 60                  // US = 60hz
#define WALL_VOLT 120                 // US = 120 V
#define DELAY_MS 1000                 // adjust this to change data transmit rate
#define MAX_RETRY 30                  // adjust this to determine how many times ESP32 tries to connect to network
#define MAX_MSG 30                    // adjust this to determine max MQTT message length
#define MAC_ADDR_LEN 17               // length of MAC address in characters (includes colons)
#define MAX_TIME_LEN 20               // length of string-formatted time

// Timestamps
// source: https://randomnerdtutorials.com/epoch-unix-time-esp32-arduino/
const char* ntpServer = "pool.ntp.org";
unsigned long epochTime; 
char displayTime[MAX_TIME_LEN];

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
String mqttDataTopicStr;                                                                // buffer for data topic name
String mqttCtrlTopicStr;                                                                // buffer for ctrl topic name
unsigned long previousMillis = 0;                                                       // used for delay

// Object constructors
ZMPT101B ZMPT(VOLT_SENSOR);                  // call ZMPT101B constructor
ACS712  ACS(CUR_SENSOR, 5, 4095, 66);        // call ACS712.h constructor for 30A variant
WiFiClient espClient;                        // call WiFi constructor
PubSubClient client(espClient);              // call MQTT constructor
WiFiManager wm;                              // call WiFi manager constructor (source: https://dronebotworkshop.com/wifimanager/)

// Function declarations - General
static unsigned long printLocalTime();
static int running_average(float data);

// Function declarations - MQTT
static int mqtt_setup();
static void msg_receive(char *topic, byte* payload, unsigned int length);

// Running average
#define DATA_COUNT 20
int count=0;                          // track number of data points summed 
float average = 0, running_total=0;   // total sum of data for averaging

/* initialization function for ESP32
 * sources: https://github.com/RobTillaart/ACS712/blob/master/examples/ACS712_20_AC/ACS712_20_AC.ino
 *          https://dronebotworkshop.com/wifimanager/
 */
void setup() { 
  Serial.begin(115200);                                       // set up baud rate for debugging
  pinMode(CUR_SENSOR, INPUT);                                 // set CUR_SENSOR to input mode
  pinMode(RELAY, OUTPUT);                                     // set RELAY pin to output mode
  Serial.println(__FILE__);

//  if (digitalRead(12) == HIGH) {
//    wm.resetSettings(); // debug: reset if pin 12 is high
//  }
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

//  delay(100);
//  int temp = ZMPT.calibrate();                              // calibrate voltage sensor (not working atm)
//  ZMPT.setZeroPoint(temp);
  ACS.autoMidPoint(1);                                        // calibrate current sensor
}

/* main function for power monitoring and data transmission/reception
 * sources: https://randomnerdtutorials.com/esp32-mqtt-publish-subscribe-arduino-ide/
 */ 
void loop() {

  unsigned long currentMillis = millis();                         // get current time

  client.loop();                                                  // keep listening on MQTT topic

  if (currentMillis - previousMillis >= DELAY_MS) {
    
    previousMillis = currentMillis; // update previous timer value

//    float volts = ZMPT.getVoltageAC(WALL_FREQ);                   // measure AC instantaneous voltage (not working atm)
    float amps = ACS.mA_AC(WALL_FREQ);                                // measure AC instantaneous current
    float watts = (WALL_VOLT * amps) / 1000;                        // calculate instantaneous power
  
    unsigned long epoch = printLocalTime();                         // get timestamp and place in local buffer

    // Add data to running average
//    int r = running_average(watts);
    //if (r > 0){
      //
      
      //watts = average;
      sprintf(mqtt_msg, "%ul, %f", epoch, watts);                     // convert number to string in string buffer
      memset(displayTime, '\0', MAX_TIME_LEN);                        // reset time buffer
      int ret = client.publish(mqttDataTopicStr.c_str(), mqtt_msg, false);  // send power data as string to MQTT data topic
      if (!ret) {
        Serial.println("loop(): unable to publish MQTT message");          
      } else {
        Serial.print("Data: ");
//        Serial.print(volts);
//        Serial.print(" ");
        Serial.print(amps);
        Serial.print(" ");
        Serial.print(watts);
        Serial.println(" | loop(): MQTT message published");
      }
    
      memset(mqtt_msg, '\0', MAX_MSG);                              // reset static buffer
    //}
  }
}

/* helper function that gets current epoch time
 * sources: https://lastminuteengineers.com/esp32-ntp-server-date-time-tutorial/
 *          https://forum.arduino.cc/t/time-library-functions-with-esp32-core/515397/4
 */
unsigned long printLocalTime(){
  time_t now;
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
//    Serial.println("Failed to obtain time");
    return -1;
  }
//  Serial.print("printLocaltime(): ");
//  Serial.println(&timeinfo, "%Y-%m-%d %H:%M:%S");
//  strftime(displayTime, MAX_TIME_LEN, "%Y-%m-%d %H:%M:%S", &timeinfo);
  return time(&now);
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
  
  mqttDataTopicStr = mqttDataTopic + WiFi.macAddress();             // print concatenated string to data topic buffer
  mqttCtrlTopicStr = mqttCtrlTopic + WiFi.macAddress();             // print concatenated string to control topic buffer
  
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

  // react to message
  String mqttCtrlTopicAck = "plux/control/ack/" + WiFi.macAddress();
  switch (msg) {
    case 49: // turning ON circuit (ASCII 1 == int 49)
      digitalWrite(RELAY, HIGH);
      client.publish(mqttCtrlTopicAck.c_str(), (const unsigned char *) "1", 2, true); // needed for server
      return;
    case 48: // turning OFF circuit (ASCII 0 == 48)
      digitalWrite(RELAY, LOW);
      client.publish(mqttCtrlTopicAck.c_str(), (const unsigned char *) "0", 2, true); // needed for server
      return;
  }
}

/*
 * Tracks running sum and returns average once 20
 * data points have been summed
 */
 static int running_average(float data){
  running_total += data;
  count++;
  if (count >= DATA_COUNT){
    // do average and reset average,count
    average = running_total/DATA_COUNT;
    running_total = 0;
    count = 0;
    return 1;
  }
  return 0;
}
