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
                print("Exiting with exception: %s" % (exc))
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
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
broadcast.settimeout(0.2)
broadcast.bind(("", 44444))
message = "['%s', '%s']" % (name,ip)
encodedMessage = str.encode(message)
while True:
        broadcast.sendto(encodedMessage, ('<broadcast>', 37020))
        print("Sent Broadcast: "+message)
        # Await connection or timeout
        try:
                server.listen(1)
                conn, addr = server.accept()
                with conn:
                        print('Connected by', addr)
                        while True:
                                # TODO: All the stuff
        except Exception as exc:
                print("No connection before timeout. Broadcasting again.")
        time.sleep(1)

