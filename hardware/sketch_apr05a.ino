int pinValue = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Initializing ESP32...");
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:
  pinValue = analogRead(A2); // ADC #1 works while WiFi is on
  Serial.println(pinValue);
  delay(500);
}
