#include "ACS712.h"

// Sources: https://create.arduino.cc/projecthub/SurtrTech/measure-any-ac-current-with-acs712-70aa85
//          https://forum.arduino.cc/t/acs712-using/361217
//          https://github.com/muratdemirtas/ACS712-arduino-1
//          https://github.com/RobTillaart/ACS712/blob/master/examples/ACS712_20_AC/ACS712_20_AC.ino

#define CUR_SENSOR A2
#define WALL_FREQ 60
#define WALL_VOLT 120                // US wall voltage standard
#define DELAY_MS 100                 // adjust delay as necessary

ACS712  ACS(A2, 5.0, 4095, 66);      // call ACS712.h constructor for 30A variant

void setup() { 
  Serial.begin(115200);              // set up baud rate for debugging
  pinMode(CUR_SENSOR, INPUT);        // set CUR_SENSOR to input mode
  Serial.begin(115200);
  Serial.println(__FILE__);

  ACS.autoMidPoint(1);               // change this value to refine accuracy
  
//  Serial.print("MidPoint: ");      // debug: print ADC midpoint and noise measurements
//  Serial.print(ACS.getMidPoint());
//  Serial.print(". Noise mV: ");
//  Serial.println(ACS.getNoisemV());

}

void loop() {
  int mA = ACS.mA_AC(WALL_FREQ);           // measure AC current
  float watts = (WALL_VOLT * mA) / 1000;   // calculate power
  
//  Serial.print("mA: ");         // debug: print current
//  Serial.println(mA);
//  Serial.print(". Form factor: ");
//  Serial.println(ACS.getFormFactor());

  Serial.print("Watts: ");        // print power
  Serial.println(watts);

  delay(DELAY_MS); 
}
