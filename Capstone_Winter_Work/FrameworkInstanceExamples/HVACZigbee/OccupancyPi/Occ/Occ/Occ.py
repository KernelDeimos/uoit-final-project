import RPi.GPIO as GPIO
import time, socket, time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)
GPIO.setup(11, GPIO.IN)

HOST = "192.168.1.40"
port = 5454
type = "Occupancy Sensor"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, port))
running = True

class OccSensor():

        def send(self, occStatus):
                byte = occStatus.encode()
                s.sendto(byte, (HOST, port))

        def run(self):
                global type
                sensType = type.encode()
                s.send(sensType)
                text = None
                print("Ready")
                while True:
                        if text is not None:
                                self.send(text)
                                text = None
                                time.sleep(3)
                                print("Ready")
                         else:
                                if GPIO.input(7):
                                        #print("7")
                                        time.sleep(0.35)
                                        if GPIO.input(11):
                                                text = "Exit"
                                                print(text)
                                elif GPIO.input(11):
                                        #print("11")
                                        time.sleep(0.35)
                                        if GPIO.input(7):
                                                text = "Entry"
                                                print(text)

occupants = OccSensor()

try:
        occupants.run()
except KeyboardInterrupt:
        s.close()

