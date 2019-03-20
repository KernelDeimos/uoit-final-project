import socket
import json

broadcastClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
broadcastClient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcastClient.bind(("", 37020))
while True:
	data, addr = broadcastClient.recvfrom(1024)
	print("received message: %s"%data)
	jsonData = json.loads(data)
	for key in jsonData:
		print("Connecting to %s" % (key))
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		HOST = jsonData[key]
		PORT = 5454
		try:
			client.connect((HOST, PORT))
			print("Sending message")
			bytesSent = client.send(str.encode(json.dumps({"code": "30"})))
			print("Message sent. Size: "+str(bytesSent))
		except Exception as exc:
			print(exc)
