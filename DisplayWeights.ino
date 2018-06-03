// DisplayWeights.ino
// Displays the readings in pounds from four load cells to the serial port.
// Author: Cole Hlava
// Last updated: May 29, 2018

#include "HX711.h"

// define calibration factors for each scale
#define calibration1 -17000
#define calibration2 -16400
#define calibration3 -16000
#define calibration4 -16100

// load cell pin definitions
HX711 scale1(2, 3);
HX711 scale2(4, 5);
HX711 scale3(6, 7);
HX711 scale4(8, 9);

void setup(){
  Serial.begin(9600);

  // calibrate scales
  scale1.set_scale(calibration1);
  scale2.set_scale(calibration2);
  scale3.set_scale(calibration3);
  scale4.set_scale(calibration4);

  // tare scales
  scale1.tare();
  scale2.tare();
  scale3.tare();
  scale4.tare();
}

void loop(){
  // print reading from scale1
  Serial.print(scale1.get_units(), 1);
  Serial.print(",");

  // print reading from scale2
  Serial.print(scale2.get_units(), 1);
  Serial.print(",");

  // print reading from scale3
  Serial.print(scale3.get_units(), 1);
  Serial.print(",");

  // print reading from scale4
  Serial.print(scale4.get_units(), 1);
  Serial.println();

  delay(200); // take readings every 200 milliseconds
}

