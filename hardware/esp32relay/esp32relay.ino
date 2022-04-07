#include <WiFi.h>

#define RELAY 15

const char* ssid = "ESP32-Soft-accessPoint";
const char* password = "yessirski";

WiFiServer server(80);

String html ="<!DOCTYPE html> \
<html> \
<body> \
<center><h1>ESP32 Soft access point</h1></center> \
<center><h2>Web Server</h2></center> \
<form> \
<button name=\"RELAYON\" button style=\"color:green\" value=\"ON\" type=\"submit\">RELAYON</button> \
<button name=\"RELAYOFF\" button style=\"color=red\" value=\"OFF\" type=\"submit\">RELAYOFF</button><br><br> \
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

void loop() {

  WiFiClient client=server.available();
  
  if(client)
  {
    String request = client.readStringUntil('\r');
    Serial.println(request);
    if(request.indexOf("ON") != -1){
      digitalWrite(RELAY, HIGH);
      Serial.println("ON");
    }
    delay(20);
    if(request.indexOf("OFF") != -1){
      digitalWrite(RELAY, LOW);
      Serial.println("OFF");
    }
    delay(20);
    client.print(html);
    client.flush();
    request="";
  }

  delay(20);
  
}
