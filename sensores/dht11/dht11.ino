#include <dht.h>

dht DHT;

#define DHT11_PIN 2

void setup(){
  Serial.begin(9600);
}

void loop()
{
  int chk = DHT.read11(DHT11_PIN);
  Serial.print("Temperatura = ");
  Serial.print(DHT.temperature);
  Serial.println(" ºC");
  Serial.print("Humedad = ");
  Serial.print(DHT.humidity);
  Serial.println(" HR");
  delay(1000);
}


