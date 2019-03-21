import socket
import json
from threading import Thread

#Listen for broadcasts when found return name of device found
#Maintain map of address for devices (name tp ip associated) - dict that
#When connective requests, connect to device from name connective gives associated to the dict produced on bc
#Once connected, new dict made of device name to socket-thread (FAB) established
#Send JSON given from connective to device name provided referenced in socket dict

deviceAddressDict = {}
connectedDeviceThreads = {}

def listenForBroadcast():
	global deviceAddressDict
	data, addr = broadcastClient.recvfrom(1024)
	jsonData = json.loads(str(data, "utf-8"))
	for key in jsonData:
		if key not in deviceAddressDict:
			deviceAddressDict[key] = jsonData[key]
			ip = jsonData[key]
			print("SAVED", deviceAddressDict)
			return key, ip

def connectToDevice(haConnectiveRequest):
	global connectedDeviceThreads
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	HOST = haConnectiveRequest
	PORT = 5454
	connectedDeviceThreads[haConnectiveRequest] = client
	try:
		client.connect((HOST, PORT))
		#print("Sending message")
		bytesSent = client.send(str.encode(json.dumps({"src": "hub", "code": "10", "msg": "request specification"})))
		print("Message sent. Size: "+str(bytesSent))
		print(client.recv(1024))
		#client.close()
	except Exception as exc:
		client.close()
		print(exc)
		exit()
	print("Connected:", connectedDeviceThreads)

class SendCommandThread(Thread):

	def __init__(self, device, command):
		Thread.__init__(self)
		self.device = device
		self.command = command

	def run(self):
		global connectedDeviceThreads
		device = self.device
		command = self.command
		client = connectedDeviceThreads[device]
		while True:
			try:
				client.send(str.encode(command))
				print("Sending command %s to device %s" % (command, device))
				response = client.recv(1024)
				stringResponse = str(response, "utf-8")
				jsonResponse = json.loads(stringResponse)
				print("**********")
				print("%s: %s" % (jsonResponse["src"], jsonResponse["output"]))
				print("**********")
			except Exception as exc:
				client.close()
				print(exc)
				exit()

broadcastClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
broadcastClient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcastClient.bind(("", 37020))

check = None

while True:

	deviceName, device = listenForBroadcast()
	# TODO: make connectToDevice handle JSON instead of string
	if check != device:
		connectToDevice(device)
	if deviceName == "Humidity Sensor":
		command = "read hum"
	elif deviceName == "Temperature Sensor":
		command = "read temp"
	else:
		print(deviceName)
		print("Fuck you you fuck stick")
		exit()
	command = json.dumps({"src": "Hub", "code": "20", "msg": command})
	commandThread = SendCommandThread(device, command)
	commandThread.start()
	#temperature = sendCommand(command)
	#print(temperature)
