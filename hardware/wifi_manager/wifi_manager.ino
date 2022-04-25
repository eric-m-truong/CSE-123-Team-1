// Simple WiFi Manager for PLUX project.
// Not completely copy-pasted; I copied the contents from the other files in the repo into one.
// In the actual code, I'm going to simplify this down quite a bit.
// - James
// Source: https://github.com/kurimawxx00/wifi-manager

#include "EEPROM.h"
#include <WebServer.h>

// WiFi login page in HTML
const char INDEX_HTML[] =
"<!DOCTYPE HTML>"
"<html>"
"<head>"
"<meta content=\"text/html; charset=ISO-8859-1\""
" http-equiv=\"content-type\">"
"<meta name = \"viewport\" content = \"width = device-width, initial-scale = 1.0, maximum-scale = 1.0, user-scalable=0\">"
"<title>ESP8266 Web Form Demo</title>"
"<style>"
"\"body { background-color: #808080; font-family: Arial, Helvetica, Sans-Serif; Color: #000000; text-align:center;}\""
"</style>"
"</head>"
"<body>"
"<h3>Enter your WiFi credentials</h3>"
"<form action=\"/\" method=\"post\">"
"<p>"
"<label>SSID:&nbsp;</label>"
"<input maxlength=\"30\" name=\"ssid\"><br>"
"<label>Key:&nbsp;&nbsp;&nbsp;&nbsp;</label><input maxlength=\"30\" name=\"password\"><br>"
"<input type=\"submit\" value=\"Save\">"
"</p>"
"</form>"
"</body>"
"</html>";

// Web server constructor using port 80
WebServer server(80);

void setup() {
  pinMode(2, OUTPUT);
  pinMode(15,INPUT); //for resetting WiFi creds
  EEPROM.begin(400);
  Serial.begin(115200);
  if(!CheckWIFICreds()){
    Serial.println("No WIFI credentials stored in memory. Loading form...");
    digitalWrite(2,HIGH);
    while(loadWIFICredsForm());
  }
}

void loop() {
  if(digitalRead(15) == HIGH){
    Serial.println("Wiping WiFi credentials from memory...");
    wipeEEPROM();
    while(loadWIFICredsForm());
  }
  digitalWrite(2,HIGH);
  delay(1000);
  digitalWrite(2,LOW);
  delay(1000);
}

void wipeEEPROM(){
  for(int i=0;i<400;i++){
    EEPROM.writeByte(i,0);
  }
  EEPROM.commit();
}

/*
 * Function to handle unknown URLs
 */
void handleNotFound() {
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
}

/*
 * Function for writing WiFi creds to EEPROM
 * Returns: true if save successful, false if unsuccessful
 */
bool writeToMemory(String ssid, String pass){
  char buff1[30];
  char buff2[30];
  ssid.toCharArray(buff1,30);
  pass.toCharArray(buff2,30); 
  EEPROM.writeString(100,buff1);
  EEPROM.writeString(200,buff2);
  delay(100);
  String s = EEPROM.readString(100);
  String p = EEPROM.readString(200);
  //#if DEBUG
  Serial.print("Stored SSID, password, are: ");
  Serial.print(s);
  Serial.print(" / ");
  Serial.print(p);
  //#endif
  if(ssid == s && pass == p){
    return true;  
  }else{
    return false;
  }
}


/*
 * Function for handling form
 */
void handleSubmit(){
  String response_success="<h1>Success</h1>";
  response_success +="<h2>Device will restart in 3 seconds</h2>";

  String response_error="<h1>Error</h1>";
  response_error +="<h2><a href='/'>Go back</a>to try again";
  
  if(writeToMemory(String(server.arg("ssid")),String(server.arg("password")))){
     server.send(200, "text/html", response_success);
     EEPROM.commit();
     delay(3000);
     ESP.restart();
  }else{
     server.send(200, "text/html", response_error);
  }
}

/*
 * Function for home page
 */
void handleRoot() {
  if (server.hasArg("ssid")&& server.hasArg("password")) {
    handleSubmit();
  }
  else {
    server.send(200, "text/html", INDEX_HTML);
  }
}

/*
 * Function for loading form
 * Returns: false if no WiFi creds in EEPROM
 */
bool loadWIFICredsForm(){
  String s = EEPROM.readString(100);
  String p = EEPROM.readString(200);
  
  const char* ssid     = "ESP32 WiFi Manager";
  const char* password = "12345678";

  Serial.println("Setting Access Point...");
  
  WiFi.softAP(ssid, password);
  
  IPAddress IP = WiFi.softAPIP();
  
  Serial.print("AP IP address: ");
  Serial.println(IP);
  
  server.on("/", handleRoot);

  server.onNotFound(handleNotFound);

  server.begin();
  
  Serial.println("HTTP server started");
 
  while(s.length() <= 0 && p.length() <= 0){
    server.handleClient();
    delay(100);
  }
  
  return false;
}

/*
 * Function checking WiFi creds in memory 
 * Returns: true if not empty, false if empty
 */
bool CheckWIFICreds(){
  Serial.println("Checking WIFI credentials");
  String s = EEPROM.readString(100);
  String p = EEPROM.readString(200);
  //#if DEBUG
  Serial.print("Found credentials: ");
  Serial.print(s);
  Serial.print("/");
  Serial.print(p);
  delay(5000);
  //#endif
  if(s.length() > 0 && p.length() > 0){
    return true;
  }else{
    return false;
  }
}
