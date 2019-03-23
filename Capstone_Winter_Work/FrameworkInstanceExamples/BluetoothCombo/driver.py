import sys, os, bluetooth, subprocess, random

targetInfo = None
nearbyDevices = None

nearbyDevices = bluetooth.discover_devices(lookup_names=True)

print(nearbyDevices)

for addr, name in nearbyDevices:
	connectCmd = input("Would you like to connect to "+name+"? (y/n)")
	if connectCmd == "y":
		print("Connecting...")
		speakerAddress = addr
		speakerName = name
		btSock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		btSock.connect((speakerAddress, 1))
	elif connectCmd == "n":
		print("Not pairing to "+name)

songs = os.listdir('/home/pi/BluetoothCombo/Music/TheGloriousSons/')

status = 0

while True:
	if status == 0:
		status = os.system("mpg123 /home/pi/BluetoothCombo/Music/TheGloriousSons/"+songs[random.randint(0,10)])
