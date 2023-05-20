from gpiozero import LED
from time import sleep

led = LED(12)

while True:
	led.on()

