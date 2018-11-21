
import Adafruit_DHT, time
from subprocess import call

while True:

	hum, temp = Adafruit_DHT.read_retry(11, 4)
	humidity = hum
	print('Humidity: {0:0.1f} %'.format(humidity))
	time.sleep(1)



