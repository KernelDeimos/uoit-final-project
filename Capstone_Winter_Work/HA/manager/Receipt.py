# -*- coding: utf-8 -*-
class Receipt:
    
    def __init__(self, source, event, command, timestamp, result):
        self.source = source
        self.event = event
        self.command = command
        self.timestamp = timestamp
        self.result = result
        self.validation = None
        
    def Validate(self, state):
        self.validation = state
        
    def Log(self):
        pass