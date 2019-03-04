# -*- coding: utf-8 -*-
import subprocess
from threading import Thread
import sys
import yaml
import time
import json

linebuffer = []
receipt_list = []
processes = {}

def reader(f,buffer):
    while True:
        line = f.readline()
        if line:
            buffer.append(line)
        else:
            break

def execute(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    
    t = Thread(target=reader,args=(p.stdout,linebuffer))
    t.daemon=True
    t.start()
    
    return p

#Test Code
config = []
cmd = ["python", "./test.py"]
config.append(cmd)

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
    for cmd in config:
        print("Executing process "+str(cmd))
        proc = execute(cmd)
        processes[str(cmd)] = proc
            
    # Start Main Loop
    print("Initializing main loop")
    while True:        
        # TODO: Confirm System State According to Configuration
        for cmd, proc in processes.items():
            status = proc.poll()
            if status is None:
                print("Process for "+cmd+" is active")
            else:
                print("Process for "+cmd+" has exited with return code "+str(status))
                input_cmd = eval(cmd)
                proc = execute(input_cmd)
                processes[cmd] = proc
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
        
        # TODO: Handle Failure Recovery
        
        time.sleep(10) #Pause included for testing purposes only
        
if __name__ == "__main__":
    main()