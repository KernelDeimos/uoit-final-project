# TODO: Add support for streaming
import socket
import time
import json
import subprocess
import netifaces as ni

# Get JSON specification
with open("/home/pi/occDriver/specifications.json", "r") as stream:
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
# Set a timeout so the socket does not block indefinitely when trying to receive data.
broadcast.settimeout(10)
broadcast.bind(("", 44444))
message = '{"%s": "%s"}' % (name,ip)
encodedMessage = str.encode(message)
while True:
        # Set time out at beginning of loop to prevent waiting for connection blocking the broadcast
        server.settimeout(1)
        # Send broadcast
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
                        server.settimeout(10)
                        print('Connected by', addr)
                        while True:
                                clientMsg = json.loads(str(conn.recv(1024), "utf-8"))
                                print(clientMsg['code'])
                                print("Src: %s Msg: %s (%s)" % (clientMsg["src"], clientMsg["msg"], clientMsg["code"]))
                                # TODO define message codes
                                if clientMsg["code"] == "10":
                                        # Send Specification
                                        try:
                                                conn.send(str.encode(json.dumps(specification)))
                                        except Exception as exc:
                                                print("Failed to send specification. Exiting with exception: %s" % (exc))
                                                exit()
                                elif clientMsg["code"] == "20":
                                        # Run Command and Return Output
                                        # Get command
                                        command = clientMsg["msg"]
                                        # Get commands.json
                                        with open("/home/pi/commands.json", "r") as stream:
                                                try:
                                                        commandList = json.load(stream)
                                                except Exception as exc:
                                                        print("Failed to open command json. Exiting with exception: %s" % (exc))
                                                        exit()
                                        # Check if command exists within known commands
                                        if command in commandList:
                                                # Execute script
                                                script = commandList[command].split(" ")
                                                p = subprocess.Popen(script, stdout=subprocess.PIPE, universal_newlines=True)
                                                output, err = p.communicate()
                                                # If Error, Create Error Response
                                                if err is not None:
                                                        response = json.dumps({"src": name, "command": command, "error": err})
                                                # Else, Create Output Response
                                                else:
                                                        response = json.dumps({"src": name, "command": command, "output": output})
                                                # Send Response
                                                try:
                                                        print(response)
                                                        conn.send(str.encode(response))
                                                except Exception as exc:
                                                        print("Failed to send command response. Exiting with exception: %s" % (exc))
                                else:
                                        # Handle unidentified code
                                        print("Could not identify code %s. Cancelling transaction." % (clientMsg["code"]))
                                        response = json.dumps({"src": name, "message": "unidentified code", "error": "unidentified code"})
                                        conn.send(str.encode(response))
                                        time.sleep(10)
                # Catch socket exceptions
        except Exception as exc:
                print("Exception in main loop: %s" % (exc))
        time.sleep(1)

