import paho.mqtt.client as mqtt
import sys
# sys.path.append('/home/pi/tesis/Codigos de dispostivos/RPi3Peter/I2C_LCD_driver')
from time import sleep
from datetime import datetime, time
from RPLCD.i2c import CharLCD


def on_message(cliente,userdata,mensaje):
    global  mensajes
    mensajes = True
    if lcd.backlight_enabled is False:
        lcd.backlight_enabled = True
    msg = mensaje.payload.decode("utf-8")
    lcd.clear()
    if msg[0] != "E":
        lcd.write_string("No depegue la \n\rtarjeta o llave")
        sleep(1)
        lcd.clear()
        lcd.write_string("Gracias!")
        sleep(1)
        lcd.clear()
        lcd.write_string(msg)
        sleep(6)
    else:
        lcd.write_string(msg)
        sleep(4)
    if medianoche <= datetime.now().time() <= amanecer and \
    lcd.backlight_enabled is True:
        lcd.backlight_enabled = False
    mensajes = False


def on_connect(cliente,userdata,flags,rc):
   print('Conectado con codigo: '+str(rc))
   cliente.subscribe("Seguridad/Pantalla",1)


broker = "127.0.0.1"
idCliente = "RPi3Peter_Pantalla"
medianoche = time(0,0,0)
amanecer = time(6,30,0)
lcd = CharLCD('PCF8574', 0x27)
mensajes = False
cliente = mqtt.Client(idCliente)
cliente.on_connect = on_connect
cliente.on_message = on_message 
cliente.connect(broker)
cliente.loop_start()

while True:
    while not mensajes:
        hora = str(datetime.now().strftime("%I:%M:%S %p"))
        lcd.clear()
        lcd.write_string(hora)
        if medianoche <= datetime.now().time() <= amanecer and \
        lcd.backlight_enabled is True:
            lcd.backlight_enabled = False
        elif not (medianoche <= datetime.now().time() <= amanecer) and \
        lcd.backlight_enabled is False:
            lcd.backlight_enabled = True
        else:
            pass
        sleep(0.95)

cliente.loop_stop()
cliente.disconnect()