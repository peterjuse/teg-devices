from Adafruit_DHT import DHT11, read
from time import sleep

sensor = DHT11
pin = 26
while True:
    humedad,temperatura = read(sensor, pin)
    print('--------------')
    if humedad is not None and temperatura is not None:
        print('Temp = {0:0.1f}C\nHR = {1:0.1f}%'.format(temperatura, humedad))
    else:
        print('Error de lectura')
    sleep(2.5)