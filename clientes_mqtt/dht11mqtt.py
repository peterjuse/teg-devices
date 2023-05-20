import paho.mqtt.client as mqtt
from Adafruit_DHT import DHT11, read
from time import sleep
from datetime import datetime

sensor = DHT11
pin = 26
broker = "RPi3PeterE"
idCliente = "RPi3Javier_DHT11"

cliente = mqtt.Client(idCliente) 
cliente.connect(broker)
cliente.loop_start()

while True:
    humedad,temperatura = read(sensor, pin)
    if humedad is not None and temperatura is not None:
        timestamp = str(datetime.now())
        lectura_temp = 'DHT11: Temp = {0:0.1f} C - Hora: '.format(temperatura)+timestamp
        timestamp = str(datetime.now())
        lectura_hr = 'DHT11: HR = {0:0.1f}% - Hora: '.format(humedad)+timestamp
        cliente.publish("Indoor/Temperatura",lectura_temp,1)
        cliente.publish('Indoor/Humedad',lectura_hr,1)
    else:
        timestamp = str(datetime.now())
        cliente.publish('Indoor/Temperatura','DHT11: Error de lectura - Hora: '+timestamp,1)
        cliente.publish('Indoor/Humedad','DHT11: Error de lectura - Hora: '+timestamp,1)
    sleep(2.5)

cliente.loop_stop()
cliente.disconnect()