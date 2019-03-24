import sys, os, bluetooth, subprocess, random, time

def confirmDevice():
	bluetoothConfirm = subprocess.getoutput("hcitool con")
	if "94:36:6E:01:B1:A5" in bluetoothConfirm.split():
		print("You are connected to the Mobile speaker.")
		time.sleep(1)
	else:
		print("You are not connected to the Mobile speaker.")

def Play():
	songs = os.listdir('/home/pi/BluetoothCombo/Music/TheGloriousSons/')
	status = 0
	while True:
		if status == 0:
			status = os.system("mpg123 /home/pi/BluetoothCombo/Music/TheGloriousSons/"+songs[random.randint(0,10)])
		else:
			print(" ")
			cont = input("Would you like to continue?(y/n)")
			if cont == "n":
				print(" ")
				print("Shutting down.")
				sys.exit()
			elif cont == "y":
				print(" ")
				print("Recalibrating...")
				time.sleep(2)
				Play()
			else:
				print(" ")
				print("What? Recalibrating anyway...")
				time.sleep(2)
				Play()


confirmDevice()
Play()
