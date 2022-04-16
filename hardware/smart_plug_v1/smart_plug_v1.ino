#include <WiFi.h>
#include <PubSubClient.h>

#include "ACS712.h"

// Network
const char* ssid         = "iPhone";
const char* password     = "yaaabruh";

// MQTT
const char* mqttServer   = "mqtts://mosquitto.projectplux.info/";
const int   mqttPort     = 8883;
const char* mqttUser     = "max";
const char* mqttPassword = "max";

// ESP32 Pins
#define CUR_SENSOR A2                // adjust as necessary
#define RELAY 27

// Constants
#define WALL_FREQ 60                 // US = 60hz
#define WALL_VOLT 120                // US = 120 V
#define DELAY_MS 100                 // adjust this to change data transmit rate
#define MAX_RETRY 30                 // adjust this to determine how many times ESP32 tries to connect to network

ACS712  ACS(A2, 5.0, 4095, 66);      // call ACS712.h constructor for 30A variant

// helper function for connecting to Internet
// source: https://randomnerdtutorials.com/esp32-useful-wi-fi-functions-arduino/
int network_setup() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("network_setup(): Connecting to WiFi ..");
  int cnt_retry = 0;
  while (WiFi.status() != WL_CONNECTED && (cnt_retry < MAX_RETRY)) {
    Serial.print('.');
    delay(1000);
    cnt_retry++;
  }
  if (cnt_retry >= MAX_RETRY) {
    Serial.println("Unable to connect, max retry limit reached");
    return 1;
  } else {
    Serial.println(WiFi.localIP());
    return 0;
  }
}

// initialization function for ESP32
// source: https://github.com/RobTillaart/ACS712/blob/master/examples/ACS712_20_AC/ACS712_20_AC.ino
void setup() { 
  Serial.begin(115200);              // set up baud rate for debugging
  pinMode(CUR_SENSOR, INPUT);        // set CUR_SENSOR to input mode
  Serial.begin(115200);
  Serial.println(__FILE__);
  
  int ret = network_setup():         // attempt network connection
  if (ret) {
    Serial.println("setup(): unable to connect to network");
    return;
  }

  ret = mqtt_setup();                // attempt MQTT server connection
  if (ret) {
    Serial.println("setup(): unable to connect to MQTT server");
    return;
  }
  
  ACS.autoMidPoint(1);               // change this value to refine accuracy
}

// main function for power monitoring and data transmission
// sources: https://randomnerdtutorials.com/esp32-mqtt-publish-subscribe-arduino-ide/
void loop() {
  int mA = ACS.mA_AC(WALL_FREQ);           // measure AC current
  float watts = (WALL_VOLT * mA) / 1000;   // calculate power
  client.loop();                 
  delay(DELAY_MS); 
}
