import re
from rfc3339 import rfc3339
from datetime import datetime
from influxdb import InfluxDBClient

cliente = InfluxDBClient(host='192.168.99.100',port=8086,username='gateway',password='gatewayiot')
cliente.create_retention_policy(name='RangoSensores',duration='7d',replication='1',database='mediciones')
archivo = open('datos.txt')
for i,linea in enumerate(archivo):
    if linea != 'Conectado con codigo resultado 0\n':
        array = linea[7:].split(' ',1)[1].split(' ',1) 
        array[1] = array[1][10:].replace("'","") 
        topico = array[0]
        payload = array[1]
        
        topico = topico.split('/')
        ubicacion = topico[0]
        medida = topico[1]
        if ubicacion == 'Indoor':
            dispositivo = 'RPi3Javier'
        elif ubicacion == 'Seguridad':
            dispositivo = 'RPi3Peter'
        else:
            dispositivo = 'Arduino+iBookG4'

        payload = payload.replace('\n','').split(' - Hora: ')
        try:
            hora = rfc3339(datetime.strptime(payload[1],'%Y-%m-%d %H:%M:%S.%f'))
        except ValueError:  
            hora = rfc3339(datetime.strptime(payload[1],'%Y-%m-%d %H:%M:%S'))
        sensor = payload[0].split(': ')
        if len(sensor)>1:
            nombre_sensor = sensor[0]
            variable = sensor[1]
        else:
            if medida == 'LedRojo': 
                nombre_sensor = 'LED-ROJO'
            elif medida == 'LedVerde':
                nombre_sensor = 'LED-VERDE'
            elif medida == 'Bombillos':
                nombre_sensor = 'LED-BLANCO'
            elif medida == 'LedRGB':
                nombre_sensor = 'LED-RGB'
            variable = sensor[0]
        if nombre_sensor not in ['HC-SR501','LED-ROJO','LED-VERDE','LED-BLANCO','LED-RGB']:
            if nombre_sensor == 'DHT11' and variable=='Error de lectura':
                variable = 'ERROR'
            else:
                variable = re.sub('[^0-9,.]','',variable[variable.find(': ')+1:])
        json = [{
                "measurement":medida,
                "tags": {
                    "host": dispositivo,
                    "region": ubicacion 
                },
                "fields": {
                    "sensor": nombre_sensor,
                    "variable": variable
                },
                "time": hora
            }]
        resultado = cliente.write_points(json,database='mediciones')
        if resultado is True:
            print('insertado correctamente')
            print(json)