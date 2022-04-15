#include <WiFi.h>

#define RELAY 15
#define SSID_MAX_LEN 32
#define PASS_MAX_LEN 20

const char* ssid = "ESP32-Soft-accessPoint";
const char* password = "yessirski";
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

void loop() {

  WiFiClient client=server.available();
  
  if(client)
  {
    String request = client.readStringUntil('\r');
    
    char request_arr[request.length() + 1];
    for (int i = 0; i < request.length(); ++i) {
      request_arr[i] = request[i];
    }
    request_arr[request.length()] = '\0';
    
    Serial.println(request);
    int index = request.indexOf("wifi_name=");
    if(index != -1){
      strncpy(wifi_id, &request_arr[index], SSID_MAX_LEN);
      Serial.println("SSID filled");
      Serial.println(wifi_id);
    }

    delay(20);
    client.print(html);
    client.flush();
    request="";
  }

  delay(20);
  
}
