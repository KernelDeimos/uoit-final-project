import socket
import json

broadcastClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
broadcastClient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
broadcastClient.bind(("", 37020))
while True:
	data, addr = broadcastClient.recvfrom(1024)
	print("received message: %s"%data)
	jsonData = json.loads(str(data, "utf-8"))
	for key in jsonData:
		print("Connecting to %s" % (key))
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		HOST = jsonData[key]
		PORT = 5454
		try:
			client.connect((HOST, PORT))
			print("Sending message")
			bytesSent = client.send(str.encode(json.dumps({"src": "hub", "code": "30", "msg": "test"})))
			print("Message sent. Size: "+str(bytesSent))
			print(client.recv(1024))
		except Exception as exc:
			print(exc)
