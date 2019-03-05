import Adafruit_DHT, time, threading, socket
from subprocess import call

HOST = "192.168.1.40"
port = 5454
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, port))
device = "HumPi connected."
running = True

class HumSensors():

	def send(self, humidity):
		byte = humidity.encode()
		s.sendto(byte, (HOST, port))

	def run(self):
		hum, temp = Adafruit_DHT.read_retry(11, 4)
		humidity = "Humidity: " + str(hum) + "%"
		print(humidity)
		while True:
			hum, temp = Adafruit_DHT.read_retry(11, 4)
			check = humidity
			humidity = "Humidity: " + str(hum) + "%"
			if check != humidity:
				self.send(humidity)
				print(humidity)
				time.sleep(1)

humidity = HumSensors()

try:
	humidity.run()
except KeyboardInterrupt:
	s.close()
