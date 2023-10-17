import csv 
import glob
import json
import os

from paho.mqtt import client as mqtt_client


broker = '127.0.0.1'
port = 1883
topic = "python/mqtt"
# Generate a Client ID with the publish prefix.
client_id = f'cliente-csv'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        print("Connected to MQTT Broker!") if rc == 0 else print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):

    os.chdir('/mnt/c/Users/peter/Desktop/TEG/Mediciones/datos_sim_2023/')
    result = glob.glob('*.{}'.format('csv'))
    for _file in result:
        with open(f"/mnt/c/Users/peter/Desktop/TEG/Mediciones/datos_sim_2023/{_file}", 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                if row == ['name', 'time', 'host', 'region', 'sensor', 'variable']:
                    continue
                msg = json.dumps({
                    "measurement_type": row[0],
                    "date": row[1],
                    "host_device": row[2],
                    "location": row[3],
                    "sensor": row[4],
                    "value": row[5]
                })
                result = client.publish(topic, msg)
                status = result[0]
                if status == 0:
                    print(f"Enviando `{msg}` al topico `{topic}`")
                else:
                    print(f"Fallo al enviar mensaje al topico {topic}")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
