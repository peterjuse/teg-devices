const int read = A0; // Sensor AO pin al pin A0 de Arduino
int value;           //  Variable que guarda el valor del agua

void setup()
{
  Serial.begin(9600); // Comunicacion serial
}

void loop()
{
  value = analogRead(read); //  Clectura por puerto analogo
  
  if (value<=480){ 
    Serial.println("Nivel de agua: 0mm"); 
  }
  else if (value>480 && value<=530){ 
    Serial.println("Nivel de agua: Entre 0mm y 5mm"); 
  }
  else if (value>530 && value<=615){ 
    Serial.println("Nivel de agua: Entre 5mm y 10mm"); 
  }
  else if (value>615 && value<=660){ 
    Serial.println("Nivel de agua: Entre 10mm y 15mm"); 
  } 
  else if (value>660 && value<=680){ 
    Serial.println("Nivel de agua: Entre 15mm y 20mm"); 
  }
  else if (value>680 && value<=690){ 
    Serial.println("Nivel de agua: Entre 20mm y 25mm"); 
  }
  else if (value>690 && value<=700){ 
    Serial.println("Nivel de agua: Entre 25mm y 30mm"); 
  }
  else if (value>700 && value<=705){ 
    Serial.println("Nivel de agua: Entre 30mm y 35mm"); 
  }
  else if (value>705){ 
    Serial.println("Nivel de agua: Entre 35mm y 40mm"); 
  }
  
  delay(5000); // Check for new value every 5 sec
}
