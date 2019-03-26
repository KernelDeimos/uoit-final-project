#!/usr/bin/env python3

# NOTE: This example is not a module; run it as a Python script.
#
#       1. Start Manager2.py
#
#       2. Run this program with the following arguments:
#          ./example.py example http://127.0.0.1:3003
#
#       2.1. Alternatively, ask another group memeber to host HA/Manager
#            and use their host address as the last parameter.

import sys, json


# Import HA/Connective bindings
from bindings import new_ll, connect, new_interpreter

# CLI arguments
arg_id = sys.argv[1]
arg_re = sys.argv[2]

# Device definition from Mozilla example:
# (https://iot.mozilla.org/wot/#web-thing-rest-api)
true = True
false = False
with open('specifications.json') as data:
	btDeviceDef = json.load(data)
	data.close()

# TODO: uuid for running example multiple times
deviceID = arg_id
print("The device id will be: {deviceID}")

# Create local interpreter and remote interpreter
ll = new_ll("../connective/connective/sharedlib/elconn.so")
ll.elconn_init(1)
remote_connective = connect(ll, arg_re.encode())
connective = new_interpreter(ll)

# Allow messages to be send to remote interpreter by prefixing
# the command "hub"
ll.elconn_link(b"hub", connective.ii, remote_connective.ii)

# So now the following both work the same:
# remote_connective.runs(": sayhello (store 'hi')")
# connective.runs("hub : sayhello (store 'hi')")

remote_connective.runl([
    # Method path
    'devices', 'add-device',
    # Method parameters
    btDeviceDef, {},
    # Custom device ID
    deviceID
])
