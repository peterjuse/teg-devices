import paho.mqtt.client as mqtt
from gpiozero import DistanceSensor
from time import sleep
from datetime import datetime

broker = "RPi3PeterE"
idCliente = "RPi3Javier_HCSR-04"
sensor = DistanceSensor(echo=24, trigger=23, max_distance=1.4)

cliente = mqtt.Client(idCliente) 
cliente.connect(broker)
cliente.loop_start()

while True:	
    distancia = int(sensor.distance * 100)
    timestamp = str(datetime.now())
    cliente.publish('Indoor/Distancia','HC-SR04: Dist = '+str(distancia)+' cm - Hora: '+timestamp,1)
    sleep(0.3)

cliente.loop_stop()
cliente.disconect()