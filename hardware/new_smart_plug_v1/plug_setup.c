#include <WiFiClientSecure.h>
#include <PubSubClient.h>

#include "ACS712.h"
#include "time.h"
#include "mqtt_setup.h"

// ESP32 Pins
#define CUR_SENSOR A2                 // adjust pins as necessary
#define ESP_RELAY 27

#define MAC_ADDR_LEN 17               // length of MAC address in characters (includes colons)

// MQTT
const char* mqttDataTopic    = "plux/data/";                  // publishing topic for plug, will be cominbed with MAC address later
const char* mqttCtrlTopic    = "plux/control/";               // subscribing topic for plug, will be cominbed with MAC address later
const char* mqttServer       = "mosquitto.projectplux.info";
const int   mqttPort         = 1883;                          // 1883 = insecure port, 8883 = secure port (via TLS)
const char* mqttUser         = "eric";
const char* mqttPassword     = "truong";

// Static variables
//static char mqtt_msg[MAX_TIME_LEN + MAX_MSG];                                           // buffer for MQTT message (timestamp + power)
static char mac_addr[MAC_ADDR_LEN];                                                     // buffer for MAC address (48 bits/8 = 6 bytes);
static char mqttDataTopicStr[10 + MAC_ADDR_LEN + 1];                                    // buffer for data topic name
static char mqttCtrlTopicStr[13 + MAC_ADDR_LEN + 1];

// Network credentials
const char* ssid         = "iPhone";                          // SSID of network to be connected to
const char* password     = "yaaabruh";                        // password of network to be connected to
//const char* ssl_server   = "www.howsmyssl.com";             // for encryption: SSL server URL
const char* ntpServer = "pool.ntp.org";

ACS712  ACS(A2, 5.0, 4095, 66);      // call ACS712.h constructor for 30A variant
WiFiClient espClient;                // call WiFi constructor
PubSubClient client(espClient);      // call MQTT constructor

// MQTT setup
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


// Network setup
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

// initialization function for ESP32
// source: https://github.com/RobTillaart/ACS712/blob/master/examples/ACS712_20_AC/ACS712_20_AC.ino
void setup() { 
  Serial.begin(115200);                                       // set up baud rate for debugging
  pinMode(CUR_SENSOR, INPUT);                                 // set CUR_SENSOR to input mode
  pinMode(ESP_RELAY, OUTPUT);                                     // set RELAY pin to output mode
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

  ret = client.subscribe(mqttCtrlTopicStr, 0);                // subscribe to MQTT control topic
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

char* get_mqttDataTopicStr(){
    return mqttDataTopicStr;
}