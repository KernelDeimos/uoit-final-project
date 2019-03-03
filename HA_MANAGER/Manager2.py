    # -*- coding: utf-8 -*-
import yaml
import time
import json
from Module import Module
from bindings import new_ll, new_interpreter

linebuffer = []
receipt_list = []
processes = []
recover = []

#Test Code
config = {}

# Import HA/Connective bindings
ll = new_ll("../ericland/connective/sharedlib/elconn.so")

# Main Loop
def main():
    # Get Configuration
    print("Accessing configuration file")
    with open("./config.yml", 'r') as stream:
        try:
            config = yaml.load(stream)
            print(config)
        except yaml.YAMLError as exc:
            print(exc)

    # Init HA/Connective Server
    initMsg = ll.elconn_init(0)
    ll.elconn_display_info(initMsg)
    connective = new_interpreter(ll)
    connective.serve_remote(b":3003") # TODO: port from env or config

    # Initialize Management Data Structures
    connective.runs(": heartbeats (@ directory)")

    # Iniitalize IoT Data Structures
    # ... TODO

    # Define system according to configuration
    print("Starting subprocesses")
    for componentConfig in config['components']:
        cmd  = componentConfig['cmd']
        name = componentConfig['name']
        id   = componentConfig['id']
        print("Executing process "+name+" with command "+str(cmd))

        # Add data structures for process management
        # TODO(eric): Update when parameter binding is added to HA/Connective
        connective.runs(f"heartbeats : '{id}' (@ heartbeat-monitor 1s)")

        # Start Process
        process = Module(id, cmd, linebuffer)
        processes.append(process)
    

    # Start Main Loop
    print("Initializing main loop")
    while True:
        # TODO: Confirm System State According to Configuration
        for proc in processes:
            status = proc.GetStatus()
            if status is not None:
                recover.append(proc)
        # TODO: Monitor System Heartbeat
        # TODO: Eric
        print("Checking Heartbeats (TODO)")
        for proc in processes:
            # TODO(any): add id field to Module, then use GetID here
            id = proc.GetName()
            result = connective.runs(
                f"heartbeats '{id}' time-since", tolist=True)
            secondsSinceLastBeat = int(result[0])

            # TODO: act on result
            print(int(result[0]))

        # Read Current Receipts
        # TODO: Prevent getting stuck in this code section
        print("Evaluating receipts in buffer")
        while True:
            if linebuffer:
                receipt = json.loads(linebuffer.pop(0))
                print("Source: {}\nEvent: {}".format(receipt["Source"], receipt["Event"]))
                receipt_list.append(receipt)
            elif not len(linebuffer):
                break
        # TODO: Check HA/Connective for New Receipts
        # TODO: Eric
        # TODO: Validate Receipts
        print("Validating Receipts (TODO)")
        while True:
            if receipt_list:
                #print(receipt_list.pop(0))
                receipt_list.pop(0)
                print("Receipt Popped") # Included for testing purposes only
            elif not len(receipt_list):
                break
        # TODO: Handle Failure Recovery
        for proc in recover:
            print("Restarting process "+proc.GetName())
            proc.Restart()

        time.sleep(10) # Included for testing purposes only

if __name__ == "__main__":
    main()
