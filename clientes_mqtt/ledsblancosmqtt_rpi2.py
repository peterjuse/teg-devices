import paho.mqtt.client as mqtt
from gpiozero import LED
from time import time
from datetime import datetime, time 

def on_message(cliente,userdata,mensaje):
    msg = mensaje.payload.decode("utf-8")
    global noche,amanecer,por_movimiento 
    
    if (msg == "ON" or \
    (msg[10:19] == "ACTIVATED" and \
    (atardecer <= datetime.now().time() <= noche or \
    medianoche <= datetime.now().time() <= amanecer)))  and \
    led.is_lit is not True:
        led.on()
        timestamp = str(datetime.now())
        cliente.publish("Seguridad/Bombillos",\
            "LED-BLANCO: ON_GOOD - Hora: "+timestamp,1)
        if msg == "ON":
            por_movimiento = False
        else:
            por_movimiento = True 

    elif (msg == "OFF" or \
    (msg[10:21] == "DEACTIVATED" and por_movimiento is True)) and \
    led.is_lit is True:
            led.off()
            timestamp = str(datetime.now())
            cliente.publish("Seguridad/Bombillos",\
                "LED-BLANCO: OFF_GOOD - Hora: "+timestamp,1)

    elif ((msg == "ON" or msg[10:19] == "ACTIVATED") \
    and led.is_lit is True) or \
    ((msg == "OFF" or msg[10:21] == "DEACTIVATED") \
    and led.is_lit is False):
        timestamp = str(datetime.now())
        cliente.publish("Seguridad/Bombillos",\
            "LED-BLANCO: LED_IN_ACTUAL_STATUS - Hora: "+timestamp,1)

    else:
        pass

def on_connect(cliente,userdata,flags,rc):
   print('Conectado con codigo: '+str(rc))
   cliente.subscribe("Seguridad/Bombillos",1)
   cliente.subscribe("Seguridad/Movimiento",1)

led = LED(12)
por_movimiento = False
atardecer = time(19,30,00)
noche = time(23,59,0)
medianoche = time(0,0,0)
amanecer = time(6,30,00)
broker = "127.0.0.1"
idCliente = "RPi3Peter_LedsBlancos"
cliente = mqtt.Client(idCliente) 
cliente.on_connect = on_connect
cliente.on_message = on_message
cliente.connect(broker)
cliente.loop_forever()