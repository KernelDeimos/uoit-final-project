import Adafruit_DHT, time, threading, socket
from subprocess import call

HOST = "192.168.1.40"
port = 5454
type = "Humidity Sensor"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, port))
running = True

class HumSensor():

        def send(self, humidity):
                byte = humidity.encode()
                s.sendto(byte, (HOST, port))

        def run(self):
                global type
                sensType = type.encode()
                s.send(sensType)
                hum, temp = Adafruit_DHT.read_retry(11, 4)
                humidity = "Humidity: " + str(hum) + "%"
                self.send(humidity)
                print(humidity)
                while True:
                        hum, temp = Adafruit_DHT.read_retry(11, 4)
                        check = humidity
                        humidity = "Humidity: " + str(hum) + "%"
                        if check != humidity:
                                self.send(humidity)
                                print(humidity)
                                time.sleep(1)

humidity = HumSensor()

try:
        humidity.run()
except KeyboardInterrupt:
        s.close()
