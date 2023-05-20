#!/usr/bin/python
from gpiozero import DistanceSensor
from time import sleep
sensor = DistanceSensor(echo=23, trigger=24)
while True:
  distancia = sensor.distance * 100
  print("Distancia : %.1f" % distancia)
  sleep(1)
