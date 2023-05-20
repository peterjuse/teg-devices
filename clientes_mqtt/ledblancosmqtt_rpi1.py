import paho.mqtt.client as mqtt
from gpiozero import LED
from datetime import datetime

def on_message(cliente,userdata,mensaje):
    msg = mensaje.payload.decode("utf-8")
    if msg == "ON" and led.is_lit is not True:
        led.on()
        timestamp = str(datetime.now())
        cliente.publish("Indoor/Bombillos","LED-BLANCO: ON_GOOD - Hora: "+timestamp,1)
    elif msg == "OFF" and led.is_lit is True:
        led.off()
        timestamp = str(datetime.now())
        cliente.publish("Indoor/Bombillos","LED-BLANCO: OFF_GOOD - Hora: "+timestamp,1)
    elif (msg == "ON" and led.is_lit is True) or \
    (msg == "OFF" and led.is_lit is False):
        timestamp = str(datetime.now())
        cliente.publish("Indoor/Bombillos","LED: LED_IN_ACTUAL_STATUS - Hora: "+timestamp,1)

def on_connect(cliente,userdata,flags,rc):
   print('Conectado con codigo: '+str(rc))
   cliente.subscribe("Indoor/Bombillos",1)

led = LED(4)
broker = "RPi3PeterE"
idCliente = "RPi3Javier_LedsBlancos"
cliente = mqtt.Client(idCliente) 
cliente.on_connect = on_connect
cliente.on_message = on_message
cliente.connect(broker)
cliente.loop_forever()
