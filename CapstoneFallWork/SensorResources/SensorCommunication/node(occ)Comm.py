import RPi.GPIO as GPIO
import time, socket, time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)
GPIO.setup(24, GPIO.IN)

HOST = "192.168.1.39"
port = 5454
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, port))
device = "PiUno connected."
running = True

def Occupant():

        while True:
                if GPIO.input(7):
                        text = "Occupancy detected"
                        byte = text.encode()
                        s.sendto(byte, (HOST, port))
                        time.sleep(5)

run = Occupant()
run.start()
