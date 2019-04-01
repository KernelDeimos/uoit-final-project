import sys, os, bluetooth, subprocess, random, time, termios, tty, select
from threading import Thread

def Connect():
	#os.system("sudo killall bluealsa")
	#os.system("pulseaudio --start")
	#time.sleep(1)
	#os.system("bluez_card.94_36_6E_01_B1_A5 a2dp_sink")
	#time.sleep(2)
	#os.system("echo connect 94:36:6E:01:B1:A5 | bluetoothctl")
	#time.sleep(2)
	#os.system("pacmd set-card-profile bluez_card.94_36_6E_01_B1_A5 a2dp_sink")
	#os.system("pacmd set-default-sink bluez_sink.94_36_6E_01_B1_A5.a2dp_sink")
	#time.sleep(3)
	confirmDevice()

def confirmDevice():
	return
	bluetoothConfirm = subprocess.getoutput("hcitool con")
	if "94:36:6E:01:B1:A5" in bluetoothConfirm.split():
		print("You are connected to the Mobile speaker.\r\n")
		time.sleep(1)
	else:
		print("\r\nYou are not connected to the Mobile speaker.\r\n")

class Speaker(Thread):
	def __init__(self):
		Thread.__init__(self)
		self.pause_event = False

	def run(self):
		while True:
			print("To disconnect enter 'quit'")
			choice = input("Would like a random choice or to choose a song? (random/choice)\r\n")
			if choice == "random":
				self.playRandom()
				break
			elif choice == "choice":
				self.playSpecific()
			elif choice == "quit":
				return
			elif choice == "s":
				self.pauseSkip("s")
			else:
				print("I didn't catch that, try again...\r\n")

	def isData(self):
		return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

	def playRandom(self):
		songs = os.listdir('/home/pi/BluetoothCombo/Music/TheGloriousSons/')
		status = 0
		#while True:
		if status == 0:
			old_settings = termios.tcgetattr(sys.stdin)
			try:
				tty.setcbreak(sys.stdin.fileno())
				#while True:
				proc = subprocess.Popen(["mplayer", "/home/pi/BluetoothCombo/Music/TheGloriousSons/"+songs[random.randint(0,10)]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
				#self.proc = proc
				#time.sleep(5)
				if self.isData():
					input = proc.stdin.read(1)
					if input == "pause":
						proc.stdin.write("pause")
						proc.stdin.flush()
					#status = os.system("mpg123 /home/pi/BluetoothCombo/Music/TheGloriousSons/"+songs[random.randint(0,10)])
			finally:
				termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
		else:
			print("no more plz")

	def playSpecific(self):
		songs = os.listdir('/home/pi/BluetoothCombo/Music/TheGloriousSons/')
		print("\r\nAvailable songs:\r\n")
		for song in songs:
			print(song)
		selection = input("\r\nWhat song would you like to listen to?")
		for song in songs:
			if selection in song:
				status = os.system("mpg123 /home/pi/BluetoothCombo/Music/TheGloriousSons/"+song)

	def getSongs(self):
		songs = os.listdir('/home/pi/BluetoothCombo/Music/TheGloriousSons/')
		availableSongs = []
		for song in songs:
			availableSongs.append(song)
		print(availableSongs)
		return availableSongs

	def pauseSkip(self, command):
		#command = input("Enter [s] to pause and [f] to skip a track")
		if command == "s":
			os.system("s")
		elif command == "f":
			os.system("f")

#Enable these to run standalone
if __name__ == '__main__':
    Connect()
    confirmDevice()
    speaker = Speaker()
    speaker.start()

