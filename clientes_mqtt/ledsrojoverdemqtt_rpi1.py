import paho.mqtt.client as mqtt
import re
from gpiozero import LED
from datetime import datetime


def on_message(cliente,userdata,mensaje):
    global status
    msg = mensaje.payload.decode("utf-8")
    distancia = int(re.sub('[ cm]','',msg[16:19]))
    if (distancia < 115 and distancia > 70) and not status:
        rojo.off()
        timestamp = str(datetime.now())
        cliente.publish("Indoor/LedRojo","LED-ROJO: OFF - Hora: "+timestamp,1)
        verde.on()
        timestamp = str(datetime.now())
        cliente.publish("Indoor/LedVerde","LED-VERDE: ON - Hora: "+timestamp,1) 
        status = True
    elif (distancia > 115 or distancia < 70) and status:
        rojo.on()
        timestamp = str(datetime.now())
        cliente.publish("Indoor/LedRojo","LED-ROJO: ON - Hora: "+timestamp,1)
        verde.off()
        timestamp = str(datetime.now())
        cliente.publish("Indoor/LedVerde","LED-VERDE: OFF - Hora: "+timestamp,1)
        status = False

def on_connect(cliente,userdata,flags,rc):
   print('Conectado con codigo: '+str(rc))
   cliente.subscribe("Indoor/Distancia",1)


rojo = LED(27)
verde = LED(17)
status = False
broker = "RPi3PeterE"
idCliente = "RPi3Javier_LedsRojoVerde"
cliente = mqtt.Client(idCliente)
cliente.on_message = on_message
cliente.on_connect = on_connect
cliente.connect(broker)
cliente.loop_forever()