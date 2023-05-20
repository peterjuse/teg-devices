import paho.mqtt.client as mqtt
from time import sleep
from datetime import datetime
from tsl2561 import TSL2561 

tsl = TSL2561(debug=1)
broker = "RPi3PeterE"
idCliente = "RPi3Javier_TSL2561"

cliente = mqtt.Client(idCliente) 
cliente.connect(broker)
cliente.loop_start()

while True:
    timestamp = str(datetime.now())
    cliente.publish('Indoor/Iluminacion','TSL2561: Lux = '+str(tsl.lux())+' - Hora: '+timestamp,1)
    sleep(10)

cliente.loop_stop()
cliente.disconect()