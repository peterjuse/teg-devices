#include <dht.h>
#include <DallasTemperature.h>
#include <OneWire.h>

//#define DHT11_PIN 7           // Pin 7 para los datos del DHT11
#define ONE_WIRE_BUS 7           // Pin 7 para los datos del DS18B20

const int LEDPin = 13;        // Pin 13 para el LED
const int PIRPin = 2;         // Pin 2 para el sensor PIR
const int FotoPin = 1;        // Pin A1 para la fotoresisencia
const int AguaPin = 0;        // Pin A0 de Arduino

int pirState = LOW;           // Estado inicial del pin del PIR
int pir = 0;                  // De inicio no hay movimiento

//dht DHT;                      // Creando el objeto para sensor DHT
int nivelAgua;                // Variable para medir el nivel de agua
int histAgua = 0;             // Variable para guardar el historico del nivel del agua
int valorFoto;                // Variable para medir el valor de la fotoresistencia

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup(){

  Serial.begin(9600);         // Configurando la comunicacion serial
  
  for (int i =9 ; i<12 ; i++)
  {
    pinMode(i, OUTPUT);       // Pines para el led RGB
  }
  pinMode(PIRPin, INPUT);     // Pin de entrada para mostrar movimiento del PIR
  pinMode(7,INPUT);
  pinMode(2,INPUT);
  
  sensors.begin();
}

void temperatura()
{
  sensors.requestTemperatures();
  float temp = sensors.getTempCByIndex(0);
  Serial.print("DS18B20: Temp = ");
  Serial.print(temp);
  Serial.println(" C");
  if(temp <  5.0){ColorLED(64,64,64);}
  else if(temp >= 5.0 && temp < 10.0){ColorLED(0,0,255);}
  else if(temp >= 10.0 && temp < 15.0){ColorLED(0,192,148);}
  else if(temp >= 15.0 && temp < 20.0){ColorLED(0,123,0);}
  else if(temp >= 20.0 && temp < 25.0){ColorLED(0,255,0);}
  else if(temp >= 25.0 && temp < 27.5){ColorLED(255,255,0);}
  else if(temp >= 27.5 && temp < 30.0){ColorLED(255,123,0);}
  else if(temp >= 30.0 && temp < 35.0){ColorLED(255,0,0);}
  else{ColorLED(255,255,255);}
}

void ColorLED(int R, int G, int B){     
  analogWrite(9 , R) ;   // LED rojo
  analogWrite(10, G) ;   // LED verde
  analogWrite(11, B) ;   // LED azul
  Serial.print("LED-RGB: (");
  Serial.print(R);
  Serial.print(",");
  Serial.print(G);
  Serial.print(",");
  Serial.print(B);
  Serial.println(")");
}

void PIR(){
   pir = digitalRead(PIRPin);
   if (pir == HIGH)   //si estÃ¡ activado
   { 
      if (pirState == LOW) // Si previamente estaba apagado
      {
        Serial.println("HC-SR501: ACTIVATED");
        pirState = HIGH;
      }
      else{Serial.println("HC-SR501: ACTIVATED");}
      
   } 
   else   // Si esta desactivado
   {
      if (pirState == HIGH)  // Si previamente estaba encendido
      {
        Serial.println("HC-SR501: DEACTIVATED");
        pirState = LOW;
      }
      else{Serial.println("HC-SR501: SLEEP");}
   }
}

//void DHT11(){
//  int chk = DHT.read11(DHT11_PIN);
//  Serial.print("Temp = ");
//  Serial.print(DHT.temperature);
//  Serial.print(" ÂºC; HR = ");
//  Serial.print(DHT.humidity);
//  Serial.println("%");
//  if(DHT.temperature <= 5.0){ColorLED(0,112,192);}
//  else if(DHT.temperature > 5.0 && DHT.temperature <= 10.0){ColorLED(146,208,80);}
//  else if(DHT.temperature > 10.0 && DHT.temperature <= 15.0){ColorLED(204,102,0);}
//  else if(DHT.temperature > 15.0 && DHT.temperature <= 20.0){ColorLED(255,255,0);}
//  else if(DHT.temperature > 20.0 && DHT.temperature <= 25.0){ColorLED(255,192,0);}
//  else if(DHT.temperature > 25.0 && DHT.temperature <= 30.0){ColorLED(255,0,0);}
//  else if(DHT.temperature > 30.0 && DHT.temperature <= 35.0){ColorLED(192,0,0);}
//  else{ColorLED(88,0,0);}
//}

void fotoresistencia(){
  valorFoto = analogRead(FotoPin);
  Serial.print("FR: Resistencia = ");
  Serial.println(valorFoto, DEC); // Intensidad de la luz  
}

void nivelSensorAgua(){
  nivelAgua = analogRead(AguaPin); //  Lectura por puerto analogo
  /*if (nivelAgua <= 130){Serial.println("Nivel de agua: 0 mm");}
  else if (nivelAgua > 130 && nivelAgua <= 160){Serial.println("Nivel de agua: Entre 0 mm y 5 mm");}
  else if (nivelAgua > 160 && nivelAgua <= 190){Serial.println("Nivel de agua: Entre 5 mm y 15 mm");}
  else if (nivelAgua > 190 && nivelAgua <= 220){Serial.println("Nivel de agua: Entre 15 mm y 20 mm");}
  else if (nivelAgua > 220){Serial.println("Nivel de agua: +20 mm");} */
  /*if(((histAgua >= nivelAgua) && ((histAgua - nivelAgua) > 5)) || ((histAgua < nivelAgua) && ((nivelAgua - histAgua) > 5)))
  {*/
    Serial.print("WL: Nivel de Agua = ");
    Serial.println(nivelAgua);
    /*histAgua = nivelAgua;
  }*/
}

void loop() {
  Serial.println("==============================================");
  PIR();
  //DHT11();
  temperatura();
  fotoresistencia();
  nivelSensorAgua();  
  delay(2500); 
}



