import serial
import time
import datetime

ser = serial.Serial(
    port='/dev/ttyACM0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
    timeout=2.5)

while True:
    linea = str(ser.readline())
    timestamp = str(datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))
    if linea[2] is not '=':
        print(linea+' -- Hora: '+timestamp+'\n')
        with open('mediciones_sensores.txt', 'a') as pyfile:
                pyfile.write(linea + ' -- Hora: ' + timestamp +'\n')
    else:
        print(linea)
        with open('mediciones_sensores.txt', 'a') as pyfile:
                pyfile.write(linea+'\n')
ser.close()