/*
   Display text on SSD (8 lines per 16 characters)
*/
#include <Wire.h>
#include <ACROBOTIC_SSD1306.h>

void setup()
{
  Wire.begin();	
  oled.init();                      // Initialze SSD1306 OLED display
  oled.clearDisplay();              // Clear screen
  oled.setTextXY(0,0);              // Set cursor position, start of line 0
  oled.putString("MJRoBot.org");
  oled.setTextXY(2,0);              // Set cursor position, start of line 2
  oled.putString("TinyML4D");
  oled.setTextXY(4,0);              // Set cursor position, start of line 4
  oled.putString("Brazil");
  oled.setTextXY(4,11);             // Set cursor position, line 4 10th character
  oled.putString("Chile");
    oled.setTextXY(6,0);             // Set cursor position, line 6 10th character
  oled.putString("----------------");
  oled.setTextXY(7,0);             // Set cursor position, line 7 10th character
  oled.putString("0123456789012345");
}

void loop()
{
}
