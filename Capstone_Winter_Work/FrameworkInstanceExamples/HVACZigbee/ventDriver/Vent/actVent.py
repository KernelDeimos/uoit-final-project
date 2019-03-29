import RPi.GPIO as GPIO
import time, socket, time, json, datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
action = 0
state = GPIO.PWM(11, 50)
#starts at closed
state.start(2.5)

class VentMotor():

	def run(self, command):
		global action
		now = datetime.datetime.now()
		if command == "open":
			self.openSA(action)
			status = ("Vent opened at "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" on "+str(now.day)+","+str(now.month)+","+str(now.year))
			response = json.dumps({"property": "vent status", "value": status})
			print(response)
			return response

		elif command == "close":
			self.closeSA(action)
			status = ("Vent closed at "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" on "+str(now.day)+","+str(now.month)+","+str(now.year))
			response = json.dumps({"property": "vent status", "value": status})
			print(response)
			return response
		else:
			#Leave vent unchanged if command unknown
			pass

	def openSA(self, action):
		global state
		if action == "0":
			print("HI")
			#open 180 degrees
			state.ChangeDutyCycle(12.5)
			status = ("Vent opened at "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" on "+str(now.day)+","+str(now.month)+","+str(now.year))
			response = json.dumps({"property": "vent status", "value": status})
			print(response)
			return response

	def closeSA(self, action):
		global state
		if action == 1:
			#close to 0 degrees (start)
			state.ChangeDutyCycle(2.5)
			status = ("Vent closed at "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" on "+str(now.day)+","+str(now.month)+","+str(now.year))
			response = json.dumps({"property": "vent status", "value": status})
			print(response)
			return response

	def open(self):
		#open 180 degrees
		now = datetime.datetime.now()
		state.ChangeDutyCycle(12.5)
		status = ("Vent opened at "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" on "+str(now.day)+","+str(now.month)+","+str(now.year))
		response = json.dumps({"property": "vent status", "value": status})
		print(response)
		return response

	def close(self):
		#close to 0 degrees
		now = datetime.datetime.now()
		state.ChangeDutyCycle(12.5)
		status = ("Vent closed at "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" on "+str(now.day)+","+str(now.month)+","+str(now.year))
		response = json.dumps({"property": "vent status", "value": status})
		print(response)
		return response


def main():
	command = "open"
	vent = VentMotor()
	return vent.run(command)

if __name__ == "__main__":
	main()


