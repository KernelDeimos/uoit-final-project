import RPi.GPIO as GPIO
import time, socket, time, json, datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)
GPIO.setup(11, GPIO.IN)

class OccSensor():

	def run(self, observation):
		while True:
			now = datetime.datetime.now()
			if GPIO.input(7):
				time.sleep(0.35)
				observation = ("Someone seen @ "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" on "+str(now.day)+","+str(now.month)+","+str(now.year))
				response = json.dumps({"property": "Occupancy", "value": observation})
				print(response)
				return response
			elif GPIO.input(11):
				time.sleep(0.35)
				observation = ("Someone seen @ "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" on "+str(now.day)+","+str(now.month)+","+str(now.year))
				response = json.dumps({"property": "Occupancy", "value": observation})
				print(response)
				return response
			response = json.dumps({"property": "Occupancy", "value": observation})
			time.sleep(0.35)
			print(response)
			observation = "No one seen"
			#return response

def main():
	obervation = "No one seen"
	occupants = OccSensor()
	return occupants.run(obervation)

if __name__ == "__main__":
	main()

observation = "No one seen"
occupants = OccSensor()
occupants.run(observation)
