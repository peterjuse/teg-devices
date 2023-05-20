import paho.mqtt.client as mqtt
from gpiozero import MotionSensor
from datetime import datetime


pir = MotionSensor(4)
broker = "127.0.0.1"
idCliente = "RPi3Peter_PIR"

cliente = mqtt.Client(idCliente) 
cliente.connect(broker)
cliente.loop_start()

while True:
    pir.wait_for_motion()
    timestamp = str(datetime.now())
    cliente.publish("Seguridad/Movimiento",
                    "HC-SR501: ACTIVATED - Hora: " + timestamp,1)
    pir.wait_for_no_motion()
    timestamp = str(datetime.now())
    cliente.publish("Seguridad/Movimiento",
                    "HC-SR501: DEACTIVATED - Hora: " + timestamp,1)
    #"HC-SR501: SlEEP"

cliente.loop_stop()
cliente.disconnect()