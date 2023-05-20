18b20
int sensorPin = 1; //Pin A1
int value = 0; 

void setup() {
  Serial.begin(9600); // Comunicacion serial
} 

void loop() {
  value = analogRead(sensorPin); 
  Serial.println(value, DEC); // Intensidad de la luz
  delay(100); 
}
