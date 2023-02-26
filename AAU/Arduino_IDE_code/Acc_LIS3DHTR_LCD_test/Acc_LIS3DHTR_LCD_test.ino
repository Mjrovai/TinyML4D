/*
 * Wio Terminal Setup
 * IMU test and Display on TFT
 * @MJRovai 23Feb23
 */

#include"LIS3DHTR.h"
#include"TFT_eSPI.h"
LIS3DHTR<TwoWire> lis;
TFT_eSPI tft;
 
void setup() {
  Serial.begin(115200);

  // Initiate LCD
  tft.begin();
  tft.setRotation(3);
  tft.fillScreen(TFT_WHITE);
  tft.setFreeFont(&FreeSansBoldOblique12pt7b);
  
  // Initiate Accelerometer
  lis.begin(Wire1);
 
  if (!lis.available()) {
    Serial.println("Failed to initialize IMU!");
    tft.drawString("Failed to initialize IMU!", 20, 10);
    while (1);
  }
  else {
    Serial.println("IMU initialized");
    tft.drawString("IMU initialized", 20, 10);
  }
  
  //Setting output data rage to 100Hz, can be set up tp 5kHz 
  lis.setOutputDataRate(LIS3DHTR_DATARATE_100HZ); 
  //Scale range set to 16g, select from 2,4,8,16g
  lis.setFullScaleRange(LIS3DHTR_RANGE_16G);    
}
 
void loop() {
  float x_values, y_values, z_values;
  x_values = lis.getAccelerationX();
  y_values = lis.getAccelerationY();
  z_values = lis.getAccelerationZ();
 
  Serial.print("X: "); Serial.print(x_values);
  Serial.print(" Y: "); Serial.print(y_values);
  Serial.print(" Z: "); Serial.print(z_values);
  Serial.println();

  tft.drawString("X:            ", 20, 60);
  tft.drawString(String(x_values), 60, 60); 
  tft.drawString("Y:            ", 20, 100);
  tft.drawString(String(y_values), 60, 100); 
  tft.drawString("Z:            ", 20, 140);
  tft.drawString(String(x_values), 60, 140); 
  delay(100);
  //tft.fillScreen(TFT_WHITE);
}
