import socket
import time
import json
import netifaces as ni

# Get JSON specification
with open("specification.json", "r") as stream:
        try:
                specification = json.load(stream)
                name = specification["name"]
        except Exception as exc:
                print("Failed to open specification json. Exiting with exception: %s" % (exc))
                exit()
# Get IP Address
ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
# Configure Host and Port for server socket
HOST = ip
PORT = 5454
# Configure broadcast socket
broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Configure server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.settimeout(1)
# Set a timeout so the socket does not block indefinitely when trying to receive data.
broadcast.settimeout(0.2)
broadcast.bind(("", 44444))
message = "['%s', '%s']" % (name,ip)
encodedMessage = str.encode(message)
while True:
        broadcast.sendto(encodedMessage, ('<broadcast>', 37020))
        print("Sent Broadcast: "+message)
        # Await connection or timeout
        try:
		# Listen for hub to connect
                server.listen(1)
		# Accept hub connection
                conn, addr = server.accept()
                with conn:
			# Remove socket time out
			server.settimeout(None)
                        print('Connected by', addr)
                        while True:
				clientMsg = json.dumps(server.recv(1024))
				print("Src: %s Msg: %s (%s)" % (clientMsg["src"], clientMsg["msg"], clientMsg["code"])
				# TODO define message codes
				if clientMsg["code"] is "10":
					server.send(specification)
				elif clientMsg["code"] is "20":
					# Get command
					command = clientMsg["msg"]
					# Get commands.json
					with open("commands.json", "r") as stream:
						try:
							commandList = json.load(stream)
						except Exception as exc:
							print("Failed to open command json. Exiting with exception: %s" % (exc))
							exit()
					# Check if command exists within known commands
					if commandList.hasKey(command):
						# Execute script
						script = commandList[command]
						p = subprocess.Popen(script, stdout=subprocess.PIPE, universal_newlines=True)
						# TODO: Add support for streaming values
						# TODO: Error handling
						output, err = p.communicate()
						if err is not None:
							server.send(str.encode(output))
				else:
					server.send(json.loads(clientMsg))
	# Catch socket exceptions
        except Exception as exc:
                print("No connection before timeout. Broadcasting again.")
        time.sleep(1)

