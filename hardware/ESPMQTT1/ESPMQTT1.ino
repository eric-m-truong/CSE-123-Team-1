#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "iPhone";
const char* password = "nathannn";
const char* mqttServer = "broker.hivemq.com";
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {

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

client.publish("esp32/esp32test", "Hello from ESP32learning");

}

void loop() {
client.loop();
client.publish("esp32/esp32test", "Hello from ESP32learning");
delay(1000);
}
