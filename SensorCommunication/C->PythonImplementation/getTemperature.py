import signal
import subprocess
from time import sleep
import Adafruit_DHT, time
from subprocess import call


class TempSensor:
	def __init__(self, executable="./temperature"):
		self.proc = subprocess.Popen(executable, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)

	def get_temperatures(self):
		for line in iter(self.proc.stdout.readline, ""):
			yield line.replace("\n", "").split(",")

t = TempSensor()

for index, x in enumerate(t.get_temperatures()):
#	if index % 20 == 0:
	print("Sensor1 Temperature: ", x[0], "C")
	print("Sensor2 Temperature: ", x[1], "C")

	hum, temp = Adafruit_DHT.read_retry(11, 4)
	humidity = hum
	print('Humidity: {0:0.1f} %'.format(humidity))
	time.sleep(1)


