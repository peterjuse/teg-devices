import paho.mqtt.client as mqtt
from datetime import datetime
from time import sleep

broker = "RPi3PeterE"
idCliente = "RPi3Peter_Reloj"
cliente = mqtt.Client(idCliente)
cliente.connect(broker)
cliente.loop_start()

while True:
    ahora = datetime.now()
    cliente.publish("Seguridad/Pantalla",ahora.strftime("%I:%M:%S %p"),1)
    sleep(0.95)

cliente.loop_stop()
cliente.disconnect()