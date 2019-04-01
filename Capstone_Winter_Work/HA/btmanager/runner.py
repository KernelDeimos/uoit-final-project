#!/usr/bin/env python3
import sys
from time import sleep
from threading import Thread

# Import Bluetooth driver
from BluetoothCombo import driver2 as driver

# Import Connective bindings
from bindings import new_ll, connect, new_interpreter

class DeviceActionListener(Thread):
    def __init__(self, command):
        Thread.__init__(self)
        self.command = command
    def run(self):
        while True:
            request = connective.runs(self.command, tolist=True)
            self.do(request)

class PlayActionListener(DeviceActionListener):
    def __init__(self, command, speaker):
        DeviceActionListener.__init__(self, command)
        self.speaker = speaker
    def do(self, request):
        self.speaker.playRandom()

class PauseActionListener(DeviceActionListener):
    def do(self, request):
        pass
        #driver.()

# CLI arguments
arg_id = sys.argv[1]
arg_re = sys.argv[2]

# Create local interpreter and remote interpreter
ll = new_ll("../connective/connective/sharedlib/elconn.so")
ll.elconn_init(1)
remote_connective = connect(ll, arg_re.encode())
connective = new_interpreter(ll)

# Allow messages to be send to remote interpreter by prefixing
# the command "hub"
ll.elconn_link(b"hub", connective.ii, remote_connective.ii)

driver.Connect()
driver.confirmDevice()
speaker = driver.Speaker()
speaker.start()


playListener = PlayActionListener("hub devices registry "+arg_id+" actions play block", speaker)
playListener.start()

while True:
    print("I'm still alive")
    sleep(2)

