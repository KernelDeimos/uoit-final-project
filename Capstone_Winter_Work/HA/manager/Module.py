# -*- coding: utf-8 -*-
import subprocess
from threading import Thread

def reader(f,buffer):
    while True:
        line = f.readline()
        if line:
            buffer.append(line)
        else:
            break

class Module:
    
    def __init__(self, name, cmd, linebuffer):
        self.name = name
        self.linebuffer = linebuffer
        self.cmd = cmd
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        self.process = p
    
        t = Thread(target=reader,args=(p.stdout,linebuffer))
        t.daemon=True
        t.start()
        self.thread = t
        
    def Restart(self):
        p = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, universal_newlines=True)
        self.process = p
    
        t = Thread(target=reader,args=(p.stdout,self.linebuffer))
        t.daemon=True
        t.start()
        self.thread = t
        
    def ReInit(self, cmd):
        self.cmd = cmd
        
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        self.process = p
    
        t = Thread(target=reader,args=(p.stdout,self.linebuffer))
        t.daemon=True
        t.start()
        self.thread = t
        
    def GetStatus(self):
        status = self.process.poll()
        if status is None:
            print("Process {} is active".format(self.name))
        else:
            print("Process for {} has exited with return code {}".format(self.name, status))
        return status
        
    def GetName(self):
        return self.name
        
    def GetCommand(self):
        return self.command
        
    def GetProcess(self):
        return self.process
    
    def SetProcess(self, process):
        self.process = process
    
    def GetThread(self):
        return self.thread
    
    def SetThread(self, thread):
        self.thread = thread