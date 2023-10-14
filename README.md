GATEWAY DE INTERNET DE LAS COSAS OPTIMIZADO PARA COMPUTACIÓN EN LA NIEBLA BAJO AMBIENTES DOMÓTICOS
Documentación, archivos de configuración, codigos de sensores y modulos desarrollados para Gateway adaptado para el Internet de las cosas

El repositorio esta divido en carpetas de documentación (documento en latex, presentacion), esquematicos (Fritzing) y los codigos de cada dispositivo. Dentro de cada dispositivo se encuentran las carpetas de los codigos referente a los sensores, actuadores, comuniación y modulos del gateway.

Los dispositivos son los siguientes:

Raspberry Pi 3 Modelo B (RPi3Peter)

Este dispositivo tiene dos tareas: de dispositivo/sistema de seguridad y de gateways IoT.

Dentro del directorio "Codigos de dispositivos/RPi3Peter se encuentran:

Cliente_MQTT: directorio con el codigo para comunicacion usando el protocolo MQTT
I2C_LCD_Driver: directorio con codigo para usar la pantalla LCD 16x2 con el protocolo I2C
Leds: directorio con el codigo para controlar los leds (bombillos)
MFRC522: directorio con el codigo para el manejo del sensor MFRC522 LEctor/Escritor RFID
PIR: directorio con el codigo para el menajo del sensor PIR (Infrarrojo Pasivo) para detección de movimiento
RasPiCam: directorio con el codigo para controlar la cámara Raspberry Pi
Raspberry Pi 3 Modelo B (RPi3Javier)

Este dispositivo tiene como tarea el medir y actuar sobre entornos bajo techo.

Dentro del directorio "Codigos de dispositivos/RPi3Javier se encuentran:

Buzzer: directorio con el codigo para control de buzzer pasivo
Cliente_MQTT: directorio con el codigo para comunicacion usando el protocolo MQTT
DHT11: directorio con el codigo para obterner las mediciones de temperatura y humedad del sensor DHT11
HC-SR04: directorio con el codigo para medir la distancia de objetos que atriesan el pasillo usando con el sensor HC-SR04
Leds: directorio con el codigo para controlar los leds (bombillos)
Servomotor: directorio con el codigo para poder controlar servomotores
TSL2561: directorio con el codigo para el sensor TSL2561 para mediciones de cantidad de luz en la habitación
iBookG4 + Arduino Uno

El Arduino Uno tiene como tarea el controlar y realizar las medidas de los sensores ambientales del exterior de una vivienda. El iBookG4 tiene como tarea obtener las mediciones a traves de comunicación serial del Arduino Uno y enviarlas a traves de la red al gateway.

Dentro del directorio "Codigos de dispositivos/iBookG4 se encuentran:

Arduino_Uno: directorio que contiene los codigos de los diversos sensores y actuadores en exteriores
Cliente_MQTT: directorio con el codigo para comunicacion usando el protocolo MQTT
