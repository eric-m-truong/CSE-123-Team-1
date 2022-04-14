#include <WiFi.h>
#include <PubSubClient.h>

#define RELAY 15
#define SSID_MAX_LEN 32
#define PASS_MAX_LEN 20

const char* ssid = "ESP32-Soft-accessPoint";
const char* password = "yessirski";
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;

char wifi_id[SSID_MAX_LEN + 1] = {0};
char wifi_password[PASS_MAX_LEN + 1] = {0};

WiFiServer server(80);

String html ="<!DOCTYPE html> \
<html> \
<body> \
<center><h1>ESP32 Soft access point</h1></center> \
<center><h2>Web Server</h2></center> \
<form> \
<p>Enter Internet Name:</p>\
<input name=\"wifi_name\"><br><br>\
<input name=\"wifi_pass\"><br><br>\
<button name=\"Submit\" button style=\"color:green\" /*value=\"Submit\"*/ type=\"submit\">Submit</button><br><br> \
</form> \
</body> \
</html>";

void Connect_WiFi()
{
WiFi.begin(ssid, password);
while(WiFi.status() != WL_CONNECTED)
{
delay(100);
}
}

void setup() {

  Serial.begin(115200);
  Serial.print("Setting soft access point mode");
  WiFi.softAP(ssid, password);
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);
  server.begin();

  pinMode(RELAY, OUTPUT);

}

void my_strncpy (char* dst, char* src, size_t n) {
  if (dst == NULL) { Serial.println("my_strncpy: dst is NULL"); }
  if (src == NULL) { Serial.println("my_strncpy: src is NULL"); }

  for (int i = 0; i < n; ++i) {
    if (src[i] == '&') {
      dst[i] = '\0';
      break;
    }
    else {
      dst[i] = src[i];
    }
  }
}

/** @brief Tries to connect to WiFi and then an MQTT broker
 *
 * @arg ssid	char array that has the WiFi SSID
 * @arg pass 	char array that has the WiFi password
 */
void connect_to_MQTT_broker (char* ssid, char* pass, char* mqtt_broker_ip, int mqtt_broker_port) {
	WiFiClient wifi_client;
	PubSubClient mqtt_client(wifi_client);
	const int MAX_RETRIES = 20;
	
	WiFi.begin(ssid, pass);
	
	while (WiFi.status() != WL_CONNECTED) {
		delay(500);
		Serial.println("Connecting to WiFi...");
	}
	
	Serial.println("Connected to WiFi network: ");
	Serial.println(ssid);
	
	mqtt_client.setServer(mqtt_broker_ip, mqtt_broker_port);
	
	while (!mqtt_client.connected()) {
		Serial.println("Connecting to MQTT Broker...");
		
		if (mqtt_client.connect("", "", "")) {
			Serial.println("Connected!");
		} else {
			Serial.print("Failed with state ");
			Serial.print(mqtt_client.state());
			delay(2000);
		}
	}
}

void loop() {

  WiFiClient client=server.available();
  
  if(client)
  {
    String request = client.readStringUntil('\r');

    // Get Request
    char request_arr[request.length() + 1];
    for (int i = 0; i < request.length(); ++i) {
      request_arr[i] = request[i];
    }
    request_arr[request.length()] = '\0';   
    Serial.println(request);

    // Parse SSID
    int index = request.indexOf("wifi_name=");
    if(index != -1){
      my_strncpy(wifi_id, &request_arr[index], SSID_MAX_LEN);
      Serial.println("SSID filled");
      Serial.println(wifi_id);
    }

    // Parse Password
    index = request.indexOf("wifi_pass=");
    if (index != -1) {
      my_strncpy(wifi_password, &request_arr[index], PASS_MAX_LEN);
      Serial.println("Password filled");
      Serial.println(wifi_password);
    }
	
	connect_to_MQTT_broker(wifi_id, wifi_password, mqtt_server, mqtt_port);

    delay(20);
    client.print(html);
    client.flush();
    request="";
  }

  delay(20);
  
}
