import paho.mqtt.client as mqtt
import serial
import re
from datetime import datetime

broker = "RPi3PeterE"
idCliente = "ibookG4"
ser = serial.Serial(
    #port='/dev/ttyACM0',\
    port='/dev/cu.usbmodem1d11',
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=2.5)

cliente = mqtt.Client(idCliente) 
cliente.connect(broker)
cliente.loop_start()

while True:
    linea = str(ser.readline().decode('utf-8'))
    linea = re.sub('[\n\r]','',linea)
    timestamp = str(datetime.now())
    linea = linea+' - Hora: '+timestamp
    print(linea)
    if linea[0] is not '=':
        if linea[0] is 'H':
            cliente.publish('Outdoor/Movimiento',linea,1)
        elif linea[0] is 'D':
            cliente.publish('Outdoor/Temperatura',linea,1)
        elif linea[0] is 'L':
            cliente.publish('Outdoor/LedRGB',linea,1)
        elif linea[0] is 'F':
            cliente.publish('Outdoor/FotoResistencia',linea,1)
        elif linea[0] is 'W':
            cliente.publish('Outdoor/NivelDeAgua',linea,1)
ser.close()

cliente.loop_stop()
cliente.disconnect()
