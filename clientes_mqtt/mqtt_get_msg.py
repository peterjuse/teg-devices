import re
import os
import sys
import paho.mqtt.client as mqtt
from rfc3339 import rfc3339
from datetime import datetime
from influxdb import InfluxDBClient


def on_connect(client, userdata, flags, rc):  # callback al conectarse al broker
    print("Conectado con codigo resultado {0}".format(str(rc)))
    cliente.subscribe("#")  # Subscripcion a # para recibir todos los topicos


def on_message(client, userdata, msg):  # callback al recibir un mensaje
    global bd
    global sensoresString
    print("Topico: " + msg.topic + " Mensaje:" + str(msg.payload))
    topico = msg.topic
    topico = topico.split('/')
    ubicacion = topico[0]
    medida = topico[1]
    if ubicacion == 'Indoor':
        dispositivo = 'RPi3Javier'
    elif ubicacion == 'Seguridad':
        dispositivo = 'RPi3Peter'
    else:
        dispositivo = 'Arduino+iBookG4'
    payload = msg.payload.decode('utf-8')
    if ubicacion == 'Seguridad' and medida == 'Pantalla':
        nombre_sensor = 'LCD-16x2'
        variable = payload
        hora = rfc3339(datetime.now())
    elif ubicacion == 'Indoor' and medida == 'Buzzer' and \
        (payload == 'ON' or payload == 'OFF'):
        nombre_sensor = 'BUZZER'
        variable = payload
        hora = rfc3339(datetime.now())
    elif medida == 'Bombillos' and (payload == 'ON' or payload == 'OFF'):
        nombre_sensor = 'LED-BLANCO'
        variable = payload
        hora = rfc3339(datetime.now())
    else:
        payload = payload.replace('\n','').split(' - Hora: ')
        try:
            hora = rfc3339(datetime.strptime(payload[1],'%Y-%m-%d %H:%M:%S.%f'))
        except ValueError:  
            hora = rfc3339(datetime.strptime(payload[1],'%Y-%m-%d %H:%M:%S'))
        sensor = payload[0].split(': ')
        nombre_sensor = sensor[0]
        variable = sensor[1]
        if nombre_sensor not in sensoresString:
            if nombre_sensor == 'DHT11' and variable=='Error de lectura':
                variable = 'ERROR'
            else:
                variable = re.sub('[^0-9,.]','',
                    variable[variable.find(': ')+1:])
        if nombre_sensor == 'RASPICAM':
            variable = variable.replace('Persona detectada = ','')
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
    try:
        bd.write_points(json)
        print('Insercion realizada correctamente')
    except Exception as e:
        print('Error al insertar dato')
    


sensoresString = [
                  'HC-SR501','LED-ROJO','LED-VERDE',
                  'LED-BLANCO','LED-RGB','MFRC522',
                  'RASPICAM','LCD-16x2','BUZZER','SG90'
                  ]
 
if __name__ == '__main__':            
    bd = InfluxDBClient(host='127.0.0.1',port=8086, username='gateway', 
                         password='MedicionesIoTDB',database='SensorData')
    cliente = mqtt.Client("dataSnifer")  
    cliente.on_connect = on_connect  # callback de conexion
    cliente.on_message = on_message  # callback al recibir un mensaje
    cliente.connect('127.0.0.1')
    cliente.loop_forever()
    os.execv(__file__,sys.argv)