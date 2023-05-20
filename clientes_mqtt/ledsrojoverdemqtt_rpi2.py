import paho.mqtt.client as mqtt
import re
from gpiozero import LED
from datetime import datetime


def on_message(cliente,userdata,mensaje):
    msg = mensaje.payload.decode("utf-8")
    if msg[10:19] == "ACTIVATED":
        rojo.off()
        timestamp = str(datetime.now())
        cliente.publish("Seguridad/LedRojo","LED-ROJO: OFF - Hora: "+timestamp,1)
        verde.on()
        timestamp = str(datetime.now())
        cliente.publish("Seguridad/LedVerde","LED-VERDE: ON - Hora: "+timestamp,1) 
        status = True
    elif msg[10:21] == "DEACTIVATED":
        rojo.on()
        timestamp = str(datetime.now())
        cliente.publish("Seguridad/LedRojo","LED-ROJO: ON - Hora: "+timestamp,1)
        verde.off()
        timestamp = str(datetime.now())
        cliente.publish("Seguridad/LedVerde","LED-VERDE: OFF - Hora: "+timestamp,1)
    else:
        pass

def on_connect(cliente,userdata,flags,rc):
   print('Conectado con codigo: '+str(rc))
   cliente.subscribe("Seguridad/Movimiento",1)


rojo = LED(5)
verde = LED(6)
broker = "127.0.0.1"
idCliente = "RPi3Peter_LedsRojoVerde"
cliente = mqtt.Client(idCliente)
cliente.on_message = on_message
cliente.on_connect = on_connect
cliente.connect(broker)
cliente.loop_forever()