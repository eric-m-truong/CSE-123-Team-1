#include <WiFiClientSecure.h>
#include <PubSubClient.h>

#include "ACS712.h"
#include "time.h"
#include "plug_setup.h"


// ESP32 Pins
#define CUR_SENSOR A2                 // adjust pins as necessary
#define RELAY 27

#define MAC_ADDR_LEN 17               // length of MAC address in characters (includes colons)

// Constants
#define WALL_FREQ 60                  // US = 60hz
#define WALL_VOLT 120                 // US = 120 V
#define DELAY_MS 1000                 // adjust this to change data transmit rate
#define MAX_RETRY 30                  // adjust this to determine how many times ESP32 tries to connect to network
#define MAX_MSG 30                    // adjust this to determine max MQTT message length
#define MAX_TIME_LEN 20               // length of string-formatted time

// Timestamps
// source: https://randomnerdtutorials.com/epoch-unix-time-esp32-arduino/
const char* ntpServer = "pool.ntp.org";
unsigned long epochTime; 
char displayTime[MAX_TIME_LEN];
/*

// Network
const char* ssid         = "iPhone";                          // SSID of network to be connected to
const char* password     = "yaaabruh";                        // password of network to be connected to
//const char* ssl_server   = "www.howsmyssl.com";             // for encryption: SSL server URL
*/
/*
// MQTT
const char* mqttDataTopic    = "plux/data/";                  // publishing topic for plug, will be cominbed with MAC address later
const char* mqttCtrlTopic    = "plux/control/";               // subscribing topic for plug, will be cominbed with MAC address later
const char* mqttServer       = "mosquitto.projectplux.info";
const int   mqttPort         = 1883;                          // 1883 = insecure port, 8883 = secure port (via TLS)
const char* mqttUser         = "eric";
const char* mqttPassword     = "truong";
*/
// Static variables
static char mqtt_msg[MAX_TIME_LEN + MAX_MSG];                                           // buffer for MQTT message (timestamp + power)
//static char mac_addr[MAC_ADDR_LEN];                                                     // buffer for MAC address (48 bits/8 = 6 bytes);
//static char mqttDataTopicStr[10 + MAC_ADDR_LEN + 1];                                    // buffer for data topic name
//static char mqttCtrlTopicStr[13 + MAC_ADDR_LEN + 1];                                    // buffer for ctrl topic name


ACS712  ACS(A2, 5.0, 4095, 66);      // call ACS712.h constructor for 30A variant
WiFiClient espClient;                // call WiFi constructor
PubSubClient client(espClient);      // call MQTT constructor

// helper function that gets current epoch time
// sources: https://lastminuteengineers.com/esp32-ntp-server-date-time-tutorial/
//         https://forum.arduino.cc/t/time-library-functions-with-esp32-core/515397/4
void printLocalTime()
{
  struct tm timeinfo;
  if(!getLocalTime(&timeinfo)){
//    Serial.println("Failed to obtain time");
    return;
  }
//  Serial.print("printLocaltime(): ");
//  Serial.println(&timeinfo, "%Y-%m-%d %H:%M:%S");
  strftime(displayTime, MAX_TIME_LEN, "%Y-%m-%d %H:%M:%S", &timeinfo);
}

/*
// helper function for connecting to Internet
// sources: https://randomnerdtutorials.com/esp32-useful-wi-fi-functions-arduino/
//          https://github.com/espressif/arduino-esp32/blob/master/libraries/WiFiClientSecure/examples/WiFiClientSecure/WiFiClientSecure.ino
int network_setup() {
  
  WiFi.mode(WIFI_STA);                                              // WiFi connection process
  WiFi.begin(ssid, password);
  Serial.print("network_setup(): Connecting to WiFi ..");
  
  int cnt_retry = 0;
  while (WiFi.status() != WL_CONNECTED && (cnt_retry < MAX_RETRY)) { // attempt connection multiple times
    Serial.print('.');
    delay(1000);
    cnt_retry++;
  }
  if (cnt_retry >= MAX_RETRY) {
    Serial.println("Unable to connect, max retry limit reached");
    return 1;
  } else {
//    espClient.setCACert(test_root_ca); // for encryption, not used
    Serial.println(WiFi.localIP());
    return 0;
  }
  
}
*/
/*
// initialization of MQTT connection
int mqtt_setup() {
  client.setServer(mqttServer, mqttPort);                         // set destination server
  while (!client.connected()) {
    Serial.println("mqtt_setup(): Connecting to MQTT...");
    if (client.connect("", mqttUser, mqttPassword)) {
      Serial.println("mqtt_setup(): client connected");
    } else {
      Serial.print("mqtt_setup(): failed with state ");           // error message, print out failure state
      Serial.println(client.state());
      delay(1000);
    }
  }

  sprintf(mqttDataTopicStr, "%s%s", mqttDataTopic, mac_addr);     // print concatenated string to data topic buffer
  sprintf(mqttCtrlTopicStr, "%s%s",  mqttCtrlTopic, mac_addr);    // print concatenated string to control topic buffer
  
//  client.publish(mqttDataTopicStr, "mqtt_stetup(): complete");  // complete connection to MQTT data topic
  Serial.println("mqtt_stetup(): complete");
  return 0;
}
*/



// initialization function for ESP32
// source: https://github.com/RobTillaart/ACS712/blob/master/examples/ACS712_20_AC/ACS712_20_AC.ino
void setup() { 
  Serial.begin(115200);                                       // set up baud rate for debugging
  pinMode(CUR_SENSOR, INPUT);                                 // set CUR_SENSOR to input mode
  pinMode(RELAY, OUTPUT);                                     // set RELAY pin to output mode
  Serial.println(__FILE__);
  
  int ret = network_setup();                                  // attempt network connection
  if (ret) {
    Serial.println("setup(): unable to connect to network");
    return;
  }
  strncpy(mac_addr, WiFi.macAddress().c_str(), MAC_ADDR_LEN); // save MAC address as string
  Serial.print("setup(): MAC address - ");
  Serial.println(WiFi.macAddress());
  
  ret = mqtt_setup();                                         // attempt MQTT server connection
  if (ret) {
    Serial.println("setup(): unable to connect to MQTT server");
    return;
  } else {
    Serial.print("setup(): publishing to ");
    Serial.println(mqttDataTopicStr);
  }

  ret = client.subscribe(get_mqttCtrlTopicStr(), 0);                // subscribe to MQTT control topic
  if (!ret) {
    Serial.println("setup(): unable to subscribe to MQTT server topic");
    return;
  } else {
    Serial.print("setup(): subscribed to ");
    Serial.println(get_mqttCtrlTopicStr());
  }

  configTime(-28800, 3600, ntpServer);                        // configure time format for display
                                                              // -28800: UTC-8
                                                              // 3600: DST offset

  ACS.autoMidPoint(1);                                        // change this value to refine accuracy
}


// helper callback function for receiving messages from server
// sources: https://pubsubclient.knolleary.net/api#callback
//          http://www.iotsharing.com/2017/08/how-to-use-esp32-mqtts-with-mqtts-mosquitto-broker-tls-ssl.html
void msg_receive(char *topic, byte* payload, unsigned int length) {

  // print topic
  Serial.print("msg_receive(): incoming message on ");
  Serial.println(topic);
  
  // de-encapsulate payload
  int msg = *payload;
  Serial.print("msg_receive(): payload - ");
  Serial.println(msg);
  switch (msg) {
    case 1: // turning ON circuit
      digitalWrite(RELAY, HIGH);
      return;
    case 2: // turning OFF circuit
      digitalWrite(RELAY, LOW);
      return;
  }
}

// main function for power monitoring and data transmission/reception
// sources: https://randomnerdtutorials.com/esp32-mqtt-publish-subscribe-arduino-ide/
void loop() {
  int mA = ACS.mA_AC(WALL_FREQ);                                // measure AC current
  float watts = (WALL_VOLT * mA) / 1000;                        // calculate power
  client.loop();                                                // keep listening on MQTT topic

  printLocalTime();                                             // get timestamp and place in local buffer
  sprintf(mqtt_msg, "%s, %d", displayTime, mA);                 // convert number to string in string buffer
  memset(displayTime, '\0', MAX_TIME_LEN);                      // reset time buffer
  
  //int ret = client.publish(mqttDataTopicStr, mqtt_msg, false);  // send power data as string to MQTT data topic
  int ret = client.publish(get_mqttDataTopicStr(), mqtt_msg, false);
  if (!ret) {
    Serial.println("loop(): unable to publish MQTT message");          
  } else {
    Serial.print("Data: ");
    Serial.print(mA);
    Serial.println(" | loop(): MQTT message published");
  }
  memset(mqtt_msg, '\0', MAX_MSG);                              // reset static buffer
  delay(DELAY_MS); 
}
