 #include <HardwareSerial.h>
 HardwareSerial MySerial(0);
 
 #define LED_BUILT_IN 21 
 
  char estate;
 
  void setup()
  {
    Serial.begin(9600);
    Serial.println("XIAO UART Reception Test");
    
    // MySerialconfiguration on pins TX=D6, RX=D7 (-1, -1 means use the default)
    MySerial.begin(9600, SERIAL_8N1, -1, -1);

  pinMode(LED_BUILT_IN, OUTPUT); // Set the pin as output
  Serial.println(MySerial.read()); 
  }
 
  void loop()
  {
    Serial.println(MySerial.read()); 
    if (MySerial.available())
    {          
      estate = MySerial.read();  
      Serial.print(estate);   
      digitalWrite(LED_BUILT_IN, LOW);   
    } 
    else
    { 
      digitalWrite(LED_BUILT_IN, HIGH); 
    }   
  }
