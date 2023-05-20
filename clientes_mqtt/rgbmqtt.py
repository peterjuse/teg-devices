import paho.mqtt.client as mqtt
import re
from gpiozero import RGBLED
from datetime import datetime, time


def on_message(cliente,userdata,mensaje):
    msg = mensaje.payload.decode("utf-8")
    if msg[7] is not "E":
        temperatura = float(re.sub('[ C]','',msg[14:16]))
        timestamp = str(datetime.now())
        if (anochecer <= datetime.now().time() <= noche or \
        medianoche <= datetime.now().time() <= amanecer) and \
        led.is_lit is True:
            led.off()
        elif (anochecer <= datetime.now().time() <= noche or \
        medianoche <= datetime.now().time() <= amanecer) and \
        led.is_lit is False:
            pass
        else:
            if temperatura <= 5.0:
                led.color = (0,0.43,0.75)
                cliente.publish('Indoor/LedRGB','LED-RGB: (0,112,192) - Hora: '+timestamp,1)
            elif temperatura > 5.0 and temperatura <= 10.0:
                led.color = (0.57,0.81,0.31)
                cliente.publish('Indoor/LedRGB','LED-RGB: (146,208,80) - Hora: '+timestamp,1)
            elif temperatura > 10.0 and temperatura <= 15.0:
                led.color = (0.8,0.4,0)
                cliente.publish('Indoor/LedRGB','LED-RGB: (204,102,0) - Hora: '+timestamp,1)
            elif temperatura > 15.0 and temperatura <= 20.0:
                led.color = (1,1,0)
                cliente.publish('Indoor/LedRGB','LED-RGB: (255,255,0) - Hora: '+timestamp,1)
            elif temperatura > 20.0 and temperatura <= 25.0:
                led.color = (1,0.75,0)
                cliente.publish('Indoor/LedRGB','LED-RGB: (255,192,0) - Hora: '+timestamp,1)
            elif temperatura > 25.0 and temperatura <= 30.0:
                led.color = (1,0,0)
                cliente.publish('Indoor/LedRGB','LED-RGB: (255,0,0) - Hora: '+timestamp,1)
            else:
                led.color = (0.75,0,0)
                cliente.publish('Indoor/LedRGB','LED-RGB: (192,0,0) - Hora: '+timestamp,1)

def on_connect(cliente,userdata,flags,rc):
   print('Conectado con codigo: '+str(rc))
   cliente.subscribe("Indoor/Temperatura",1)


led = RGBLED(5,6,13)
anochecer = time(23,45,00)
noche = time(23,59,0)
medianoche = time(0,0,0)
amanecer = time(6,30,00)
broker = "RPi3PeterE"
idCliente = "RPi3Javier_rgb"
cliente = mqtt.Client(idCliente)
cliente.on_message = on_message
cliente.on_connect = on_connect
cliente.connect(broker)
cliente.loop_forever()
