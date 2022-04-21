#include "plug_setup.h"

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
