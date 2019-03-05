import signal, subprocess, threading, time, socket
from time import sleep
from subprocess import call

HOST = "192.168.1.40"
port = 5454
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((HOST, port))
running = True


class TempSensors(threading.Thread):

	def get_temperatures(self):
		for line in iter(self.proc.stdout.readline, ""):
			yield line.replace("\n", "").split(",")

	def run(self):
		executable="./temperature"
		self.proc = subprocess.Popen(executable, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)
		while True:
			text = 69 #just a starter for i2c initialization
			for index, x in enumerate(self.get_temperatures()):
				check = text
				text = "Temperature: " + x[0] + "C"
				if check != text:
					byte = text.encode()
					s.sendto(byte, (HOST, port))
					time.sleep(3)

temperature = TempSensors()
temperature.start()



