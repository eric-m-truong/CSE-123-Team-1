#include <WiFi.h>
#include <PubSubClient.h>

#include "ACS712.h"

// Sources: https://create.arduino.cc/projecthub/SurtrTech/measure-any-ac-current-with-acs712-70aa85
//          https://forum.arduino.cc/t/acs712-using/361217
//          https://github.com/muratdemirtas/ACS712-arduino-1
//          https://github.com/RobTillaart/ACS712/blob/master/examples/ACS712_20_AC/ACS712_20_AC.ino

#define CUR_SENSOR A2
#define WALL_FREQ 60
#define WALL_VOLT 120                // US wall voltage standard
#define DELAY_MS 500                 // adjust delay as necessary
#define MSG_MAX 50

ACS712  ACS(A2, 5.0, 4095, 66);      // call ACS712.h constructor for 30A variant

//MQTT
const char* ssid = "iPhone";
const char* password = "nathannn";
const char* mqttServer = "broker.hivemq.com";
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";
char msg[MSG_MAX];                   // buffer for msg

WiFiClient espClient;
PubSubClient client(espClient);

//void init_pin() {
//  pinMode(15, OUTPUT);
//}

void mqtt_setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }

  Serial.println("Connected to the WiFi network");

  client.setServer(mqttServer, mqttPort);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");

  if (client.connect("", mqttUser, mqttPassword )) {

    Serial.println("connected");

  } else {

  Serial.print("failed with state ");
  Serial.print(client.state());
  delay(2000);

    }
  }
}

void setup() { 
  Serial.begin(115200);              // set up baud rate for debugging
  pinMode(CUR_SENSOR, INPUT);        // set CUR_SENSOR to input mode
  Serial.begin(115200);
  Serial.println(__FILE__);

  ACS.autoMidPoint(1);               // change this value to refine accuracy
  // init_pin();
  // digitalWrite(15, HIGH);
  // delay(1000)
}

void loop() {
  int mA = ACS.mA_AC(WALL_FREQ);           // measure AC current
  float watts = (WALL_VOLT * mA) / 1000;   // calculate power

  char msg[MSG_MAX];                       // buffer for msg
  memset(msg, "\0", MSG_MAX);
  sprintf(msg, "%f\n", watts);

  client.loop();                           // MQTT message publishing
  client.publish("esp32/esp32test", "Hello from ESP32learning");
  delay(DELAY_MS);
}
