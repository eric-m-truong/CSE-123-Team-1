#include "plug_setup.h"
#include <Arduino.h>

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


char* get_mqttCtrlTopicStr(){
    return mqttCtrlTopicStr;
}

char* get_mqttDataTopicStr(){
    return mqttDataTopicStr;
}
