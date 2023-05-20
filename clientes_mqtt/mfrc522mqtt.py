import sys
sys.path.append('/home/pi/tesis/Codigos de dispostivos/RPi3Peter/MFRC522_Module')
import SimpleMFRC522
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from datetime import datetime
from time import sleep


def on_connect(cliente,userdata,flags,rc):
   print('Conectado con codigo: '+str(rc))
   cliente.subscribe("Seguridad/LectorRFID",1)


broker = "127.0.0.1"
idCliente = "RPi3Peter_RFID"
cliente = mqtt.Client(idCliente)
cliente.on_connect = on_connect
cliente.connect(broker)
cliente.loop_start()

while True:
    lector = SimpleMFRC522.SimpleMFRC522()
    try:
        id, contenido = lector.read()
        print("ID: "+str(id)+" Contenido: "+contenido)
        if contenido == "AUTH ERROR!!" \
        or contenido == "AUTH ERROR(status2reg & 0x08) != 0" \
        or not contenido:
            cliente.publish('Seguridad/Pantalla','Error de Lectura')
            timestamp = str(datetime.now())
            cliente.publish('Seguridad/LectorRFID',
                            'MFRC522: LECTURA_ERROR - Hora: ' + timestamp)
        else:
            display_msg = contenido.split(' ',1)[0]
            print(display_msg)
            cliente.publish('Seguridad/Pantalla',
                            'Bienvenido a\n\rcasa ' + display_msg)
            timestamp = str(datetime.now())
            cliente.publish('Seguridad/LectorRFID',
                            'MFRC522: LECTURA_OK - Hora: ' + timestamp)
            # contenido = contenido.split('-')
            # contenido[2] = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            # lector.write(' '.join(contenido))
    finally:
        print("Error de Lectura")
        # cliente.publish('Seguridad/Pantalla','Error de Lectura')
        # timestamp = str(datetime.now())
        # cliente.publish('Seguridad/LectorRFID',
        #                 'MFRC522: LECTURA_ERROR - Hora: ' + timestamp)
    GPIO.cleanup()
    sleep(1)

cliente.loop_stop()
cliente.disconect()