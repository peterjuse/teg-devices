#!/usr/bin/python

from Adafruit_DHT import DHT11, read_retry
from tsl2561 import TSL2561
from gpiozero import DistanceSensor
from time import sleep
from datetime import datetime

dht11 = DHT11
hcsr04 = DistanceSensor(echo=23,trigger=24)
tsl = TSL2561(debug=1)

while True:
    timestamp = str(datetime.now())
    print "-------------------------------"
    print timestamp
    humedad, temperatura = read_retry(dht11, 26)
    if humedad is not None and temperatura is not None:
        print('DHT11: Temp = {0:0.1f} C\nHR = {1:0.1f} %'.format(temperatura, humedad))
    else:
        print('DHT11: Error')

    distancia = hcsr04.distance * 100
    print("HC-SR04: Dist = %.1f" % distancia)

    lux = tsl.lux()
    print("TSL2561: Lux = "+str(lux))
    sleep(2.5)

