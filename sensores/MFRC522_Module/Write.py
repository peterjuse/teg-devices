#!/usr/bin/env python

import RPi.GPIO as GPIO
import SimpleMFRC522

reader = SimpleMFRC522.SimpleMFRC522()

try:
        text = raw_input('Datos nuevos:')
        print("Coloque el Tag RFID para escribir")
        reader.write(text)
        print("Datos escritos")
finally:
        GPIO.cleanup()
