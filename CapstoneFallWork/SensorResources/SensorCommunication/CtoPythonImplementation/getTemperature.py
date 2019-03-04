import signal, subprocess, threading
from time import sleep
import Adafruit_DHT, time
from subprocess import call


class TempSensors(threading.Thread):

	def get_temperatures(self):
		for line in iter(self.proc.stdout.readline, ""):
			yield line.replace("\n", "").split(",")

	def run(self):
		executable="./temperature"
		self.proc = subprocess.Popen(executable, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
		while True:
			for index, x in enumerate(self.get_temperatures()):
				print("Sensor1 Temperature: ", x[0], "C")
				print("Sensor2 Temperature: ", x[1], "C")

class HumSensor(threading.Thread):
	def stopwatch(self, seconds):
		start = time.time()
		time.clock()
		elapsed = 0
		while elapsed <= seconds:
			elapsed = time.time() - start
		return elapsed

	def run(self):
		while True:
			hum, temp = Adafruit_DHT.read_retry(11, 4)
			humidity = hum
			kill = self.stopwatch(5)
			while kill != 5:
				print('Humidity: {0:0.1f} %'.format(humidity))
				print("From {}".format(self.getName())
				break

t = TempSensors()
h = HumSensor()

count = 0

h.start()
t.start()



