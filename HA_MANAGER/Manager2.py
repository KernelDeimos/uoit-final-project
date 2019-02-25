# -*- coding: utf-8 -*-
import yaml
import time
import json
from Module import Module

linebuffer = []
receipt_list = []
processes = []
recover = []

#Test Code
config = {}
cmd = ["python", "./test.py"]
config["Test"] = cmd

# TODO: Initialize HA/Connective
# TODO: Eric

# Main Loop
def main():
    # Get Configuration
    print("Accessing configuration file")
    with open("config.yml", 'r') as stream:
        try:
            print(yaml.load(stream))
        except yaml.YAMLError as exc:
            print(exc)        
    # Define system according to configuration
    print("Starting subprocesses")
    for name, cmd in config.items():
        print("Executing process "+name+" with command "+str(cmd))
        process = Module(name, cmd, linebuffer)
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
            proc.Restart()
        
        time.sleep(10) # Included for testing purposes only
        
if __name__ == "__main__":
    main()