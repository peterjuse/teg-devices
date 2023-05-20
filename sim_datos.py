import re
import os
import sys
import csv

#from rfc3339 import rfc3339
from datetime import datetime, timedelta
from influxdb import InfluxDBClient

token = 'z9B0hlRQEvQqC9Y59MpiU1DH32pnwtJl5N9mAMOUhQ7HZIO32zsUOxDoNPis3_vdpku7W69sMlzeJJYXWU7Vfg=='

bd = InfluxDBClient(host='127.0.0.1',port=8086, username='gateway', 
                    password='MedicionesIoTDB',database='SensorData')


with open(sys.argv[1]) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            pass
        else:
            medida = row[0]
            dispositivo = row[2]
            ubicacion = row[3]
            nombre_sensor = row[4]
            variable = row[5]
            hora = row[1]
            # Aqui va e; cambio de strimg a date
            hora = datetime.strptime(hora, '%Y-%m-%dT%H:%M:%SZ')
            # Sumar el delta de dias adecuados
            hora = hora +  timedelta(days=1000)
            # devolver a string para poder insertar en la base de datos
            hora = hora.strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
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
            print('dato #'+str(line_count-1)+': ')
            line_count += 1
            # print(json)
        try:
            bd.write_points(json)
            print('Insercion realizada correctamente')
        except Exception as e:
            print('Error al insertar dato')
           

