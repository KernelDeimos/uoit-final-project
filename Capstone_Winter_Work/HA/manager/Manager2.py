# -*- coding: utf-8 -*-
import yaml
import time
import json
from Module import Module
from bindings import new_ll, new_interpreter
from threading import Thread

linebuffer = []
receipt_list = []
processes = []
recover = []

#Test Code
config = {}

# Import HA/Connective bindings
ll = new_ll("../connective/connective/sharedlib/elconn.so")

class PackageEventThread(Thread):
    def __init__(self, connective):
        self.connective = connective
    def run(self):
        config = self.connective.runs('hub events new-package block',
            tolist=True)
        package_name = config['packaged_id']
        for command in config['commands']
            id = "%s-%s" % (command, package_name)
            cmd = config['commands'][command]
            try:
                process = Module(id, cmd, linebuffer, package=True, package_name=package_name)
                processes.append(process)
            except CommandNotRecognized:
                #TODO: Handle this
                print("Command not recognized")

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
    initMsg = ll.elconn_init(1)
    ll.elconn_display_info(initMsg)
    connective = new_interpreter(ll)
    connective.serve_remote(b":3111") # TODO: port from env or config

    # Initialize Management Data Structures
    connective.runs(": heartbeats (@ directory)")

    # Initialize event queue directory
    connective.runs(": events (@ directory")
    connective.runs("events : new-package (@ requests)")

    # Iniitalize IoT Data Structures
    connective.runs(": devices (@ directory)")
    connective.runs("include device ($ devices)")

    # Define system according to configuration
    print("Starting subprocesses")
    for componentConfig in config['components']:
        cmd  = componentConfig['cmd']
        name = componentConfig['name']
        id   = componentConfig['id']
        print("Executing process "+name+" with command "+str(cmd))

        # re-write attributes in cmd to include remote address and app id
        for x in range(len(cmd)):
            cmd[x] = cmd[x].replace('<id>', id)
            # TODO: this address is currently hard-coded
            cmd[x] = cmd[x].replace('<remote>', "http://127.0.0.1:3111")

        print("exe: ",cmd)

        # Add data structures for process management
        # TODO(eric): Update when parameter binding is added to HA/Connective
        connective.runs("heartbeats : '"+id+"' (@ heartbeat-monitor 1s)")

        # Start Process
        try:
            process = Module(id, cmd, linebuffer)
            processes.append(process)
        except CommandNotRecognized:
            # TODO: Handle this
            print("Command not recognized")

    doNotCollect200 = PackageEventThread(connective).start()

    # Start Main Loop
    print("Initializing main loop")
    while True:
        # TODO: Confirm System State According to Configuration
        #for proc in processes:
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
                "heartbeats '"+id+"' time-since", tolist=True)
            secondsSinceLastBeat = int(result[0])

            # TODO: act on result
            print(int(result[0]))

        # Read Current Receipts
        # TODO: Prevent getting stuck in this code section
        print("Evaluating receipts in buffer")
        while True:
            if linebuffer:
                try:
                    receipt = json.loads(linebuffer.pop(0))
                    print("Source: {}\nEvent: {}".format(receipt["Source"], receipt["Event"]))
                    receipt_list.append(receipt)
                except json.decoder.JSONDecodeError:
                    pass
            elif not len(linebuffer):
                break

        # TODO: Validate Receipts
        print("Validating Receipts (TODO)")
        while True:
            if receipt_list:
                #print(receipt_list.pop(0))
                item = receipt_list.pop(0)
                print(item)

                # TODO: possible key error ('Command' missing) would crash
                #       the manager
                receipt = connective.runs(
                    "get-receipt "+item['Command'], tolist=True)

                print("Receipt Popped: ", receipt) # Included for testing purposes only

                # TODO: if status is "started", push it to the back of the
                #       receipt list and track how long this command is taking

                # TODO: if status is neither "started" nor "complete", this
                #       may indicate a problem:
                #
                #       unrecognized:
                #       - Maybe HA/Connective just hasn't received it yet
                #              (likely if the receipt was just generated)
                #       - Maybe the component's connection to Connective has
                #         failed (likely if it's been a while)
                #
                #       inconsistent:
                #       - Internal error from HA/Connective; a failure should
                #         be reported. ("this should never happen" type error)
            elif not len(receipt_list):
                break
        # TODO: Handle Failure Recovery
        for proc in recover:
            print("Restarting process "+proc.GetName())
            proc.Restart()

        time.sleep(10) # Included for testing purposes only

if __name__ == "__main__":
    main()
