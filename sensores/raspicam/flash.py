from gpiozero import LED
from time import sleep

led = LED(13)

while True:
	led.on()

