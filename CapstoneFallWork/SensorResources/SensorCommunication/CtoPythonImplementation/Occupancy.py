import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(22, GPIO.IN)
GPIO.setup(24, GPIO.IN)

def Entry_Exit():

	while True:
		if GPIO.input(22):
			time.sleep(0.5)
			if GPIO.input(24):
				print("Entry")
				time.sleep(3)
		if GPIO.input(24):
			time.sleep(0.5)
			if GPIO.input(22):
				print("Exit")
				time.sleep(3)



