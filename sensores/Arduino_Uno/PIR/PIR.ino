
const int LEDPin= 13;
const int PIRPin= 2;
int value= 0;
 
void setup()
{
  pinMode(LEDPin, OUTPUT);
  pinMode(PIRPin, INPUT);
  Serial.begin(9600);
}
 
void loop()
{
  value= digitalRead(PIRPin);
 
  if (value == HIGH)
  {
    digitalWrite(LEDPin, HIGH);
    Serial.println("Activado");
  }
  else
  {
    digitalWrite(LEDPin, LOW);
    Serial.println("Desactivado");
  }
  delay()
}
