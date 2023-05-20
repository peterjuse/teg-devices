import paho.mqtt.client as mqtt
import sys
import re 
sys.path.append('/home/pi/tesis/Codigos de dispostivos/RPi3Javier/buzzer')
from buzzer_lib import setup, play_music, destroy
from time import sleep
from datetime import datetime


def on_message(cliente,userdata,mensaje):
    msg = mensaje.payload.decode("utf-8")
    if msg == "ON":
        global buzzer_pin
        try:
            setup(buzzer_pin)
            timestamp = str(datetime.now())
            cliente.publish('Indoor/Buzzer','Buzzer: BUZZER_ON - Hora: '+timestamp,1)
            play_music(buzzer_pin)
            sleep(2)
            timestamp = str(datetime.now())
            cliente.publish('Indoor/Buzzer','Buzzer: BUZZER_OFF - Hora: '+timestamp,1)
            destroy()
        except KeyboardInterrupt:
            destroy()
    else:
        pass

def on_connect(cliente,userdata,flags,rc):
    print('Conectado con codigo: '+str(rc))
    cliente.subscribe("Indoor/Buzzer",1)

buzzer_pin = 22
broker = "RPi3PeterE"
idCliente = "RPi3Javier_Buzzer"
cliente = mqtt.Client(idCliente)
cliente.on_message = on_message
cliente.on_connect = on_connect
cliente.connect(broker)
cliente.loop_forever()