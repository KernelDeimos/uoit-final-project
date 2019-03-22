#TODO: Implement buffers properly

import socket
import json
from threading import Thread

# Broadcast Client Constants
BROADCAST_PORT = 37020
BROADCAST_TIMEOUT = 10

# Device Client Constants
DEVICE_PORT = 5454

# Dictionary of found devices in format {<name>: <ip>}
deviceAddressDict = {}
# Dictionary of connected devices in format {<name>: <DeviceClient object>}
connectedDeviceDict = {}

# Message to request device specification.json
GET_SPECIFICATION_MSG = str.encode(json.dumps({"src": "hub", "code": "10", "msg": "request specification"}))

class BroadcastClient():
	""" 
	Client for receiving and handling compatible device broadcasts
	"""

	def __init__(self, port):
		# Create UDP Socket
		self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# Set Socket Options
		self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		# Set timeout to prevent blocking
		self.client.settimeout(BROADCAST_TIMEOUT)
		# Bind to broadcast port
		self.client.bind(("", port))

	def listenForBroadcast(self):
		# Get global device address dictionary
		global deviceAddressDict
		# Receive broadcast on broadcast client
		data, addr = self.client.recvfrom(1024)
		# Convert data to JSON object
		jsonData = json.loads(str(data, "utf-8"))
		# Get device name (key) and device addres
		for key in jsonData:
			# Check if in existing dictionary
			if key not in deviceAddressDict:
				# Add device to dictionary
				deviceAddressDict[key] = jsonData[key]
				ip = jsonData[key]
				print("SAVED", deviceAddressDict)
				# Return name and address
				return key, ip
			else:
				# Return None values
				return None, None

class DeviceClient(Thread):

	def __init__(self, name, address, port):
		# Initialize Thread
		Thread.__init__(self)
		# Set attributes
		self.name = name
		self.address = address
		self.port = port
		# TODO: Didn't know how else to set this paramter
		self.command = None

	def createSocket(self):
		# Create client for new device
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			# Connect to device
			client.connect((address, port))
			# Register device in connected device dictionary
			self.register()
			# Send message to get device specification
			client.send(GET_SPECIFICATION_MSG)
			# TODO; Handle specification through connective
		except Exception as exc:
			# TODO: Handle exceptions
			print("[Device Client %s] An unexpected exception has occurred: %s" % (self.name, exc)


	def registerDeviceClient(self):
		# Get global connected device thread dictionary
		global connectedDeviceDict
		# Register Device
		connectedDeviceDict[self.name] = self

	def buildCommand(self, command):
		self.command = str.encode(json.dumps({"src": "hub", "code": "20", "msg": command}))


	def run(self):
		# Get command and socket
		command = self.command
		client = self.client
		# Send Command
		try:
			# Send command to device
			client.send(command)
			print("Sending command %s to device %s" % (command, device))
			# Receive device response
			response = json.loads(str(client.recv(1024), "utf-8"))
			# TODO: Handle response through connective
			print("**********")
			print("%s: %s" % (response["src"], response["output"]))
			print("**********")
		except Exception as exc:
			# TODO: Handle exceptions
			client.close()
			print(exc)
			exit()

# Main Loop
def main():
	# Create broadcast client
	broadcastClient = BroadcastClient(BROADCAST_PORT)
	# Enter Main Loop
	while True:
		# Liste for broadcast
		try:
			deviceName, deviceAddress = broadcastClient.listenForBroadcast()
		except socket.timeout as timeout:
			print("[Broadcast Client] A timeout has occurred without finding a new broadcast.")
		except socket.error as error:
			print("[Broadcast Client] A socket error has occurrred: %s" (error))
		except Exception as exc:
			print("[Broadcast Client] An unexpected exception has occurred: %s" % (exc))

#broadcastClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
#broadcastClient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#broadcastClient.bind(("", 37020))

#check = None

#while True:

	#deviceName, device = listenForBroadcast()
	# TODO: make connectToDevice handle JSON instead of string
	#if check != device:
		#connectToDevice(device)
	#if deviceName == "Humidity Sensor":
		#command = "read hum"
	#elif deviceName == "Temperature Sensor":
		#command = "read temp"
	#else:
		#print(deviceName)
		#print("Fuck you you fuck stick")
		#exit()
	#command = json.dumps({"src": "Hub", "code": "20", "msg": command})
	#commandThread = SendCommandThread(device, command)
	#commandThread.start()
	#temperature = sendCommand(command)
	#print(temperature)
