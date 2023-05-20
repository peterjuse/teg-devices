from gpiozero import LED
from time import sleep

rojo = LED(5)
verde = LED(6)

while True:
	verde.off()
	rojo.on()
	sleep(1)
	rojo.off()
	verde.on()
	sleep(1)
