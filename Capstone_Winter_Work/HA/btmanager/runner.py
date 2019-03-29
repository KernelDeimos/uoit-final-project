#!/usr/bin/env python3
import sys
from time import sleep
from threading import Thread

# Import Bluetooth driver
from BluetoothCombo import driver

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
    def do(self, request):
        driver.Play()

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

playListener = PlayActionListener("hub devices registry "+arg_id+" actions play block")
playListener.start()
        
driver.confirmDevice()

while True:
    print("I'm still alive")
    sleep(2)

