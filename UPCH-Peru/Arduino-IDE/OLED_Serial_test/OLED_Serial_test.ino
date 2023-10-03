
void setup()
{
  Serial1.begin(9600);
  Serial1.println("Serial Test");
  pinMode(LED_BUILTIN, OUTPUT);
}

int number;
void loop()
{
  Serial1.print("Value: ");
  Serial1.println(number);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
  number++;

}