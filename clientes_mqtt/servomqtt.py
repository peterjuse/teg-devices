import paho.mqtt.client as mqtt
import re
from gpiozero import Servo
from time import sleep
from datetime import datetime 


def on_message(cliente,userdata,mensaje):
    global status
    msg = mensaje.payload.decode("utf-8")
    distancia = int(re.sub('[ cm]','',msg[16:19]))
    timestamp = str(datetime.now())
    if (distancia < 50) and not status:
        servo.mid()
        sleep(0.5)
        servo.max()
        cliente.publish("Indoor/Servomotor","SG90: SERVO_ON - Hora: "+timestamp,1)
        status = True
    elif(distancia > 50) and status:
        servo.mid()
        sleep(0.5)
        servo.min()
        cliente.publish("Indoor/Servomotor","SG90: SERVO_OFF - Hora: "+timestamp,1)
        status = False
    else:
        servo.detach()

def on_connect(cliente,userdata,flags,rc):
   print('Conectado con codigo: '+str(rc))
   cliente.subscribe("Indoor/Distancia",1)


myCorrection=0.45
maxPW=(2.0+myCorrection)/1000
minPW=(1.0-myCorrection)/1000
servo = Servo(12,min_pulse_width=minPW,max_pulse_width=maxPW)
status = False
broker = "RPi3PeterE"
idCliente = "RPi3Javier_Servo"
cliente = mqtt.Client(idCliente)
cliente.on_message = on_message
cliente.on_connect = on_connect
cliente.connect(broker)
cliente.loop_forever()