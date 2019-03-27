# -*- coding: utf-8 -*-
import subprocess
import os
from threading import Thread

BASE_PATH = "./../server/packages"

def reader(f,buffer):
    while True:
        line = f.readline()
        if line:
            buffer.append(line)
        else:
            break

class Error(Exception):
    """Base Class for Custom Exceptions"""
    pass

class CommandNotRecognized(Error):
    """Raised when command is invalid"""
    pass

class Module:

    def __init__(self, name, cmd, linebuffer, package=False, package_name=""):
        self.name = name
        self.linebuffer = linebuffer
        self.cmd = cmd
        self.package = package
        self.package_name = package_name

        if not package:
            if cmd[0] == 'exec':
                p = subprocess.Popen(cmd[1], stdout=subprocess.PIPE, universal_newlines=True)
                self.process = p
            else:
                raise CommandNotRecognized
        else:
            if cmd[0] == 'docker':
                image_path = os.path.join(BASE_PATH, package_name, cmd[1])
                load_command = ['docker', 'load', image_path]
                docker_load = subprocess.Popen(load_command, stdout=subprocess.PIPE, universal_newlines=True)
                returncode = p.wait()
                if not returncode == 0:
                    command = ['docker', 'run', cmd[2]]
                    for arg in cmd[3]:
                        run_command.append(arg)
                    p = subprocess.Popen(run_command, stdout=subprocess.PIPE, universal_newlines=True)
                    self.process = p
            else:
                raise CommandNotRecongized

        t = Thread(target=reader,args=(p.stdout,linebuffer))
        t.daemon=True
        t.start()
        self.thread = t

    def Restart(self):
        cmd = self.cmd
        package = self.package
        package_name = self.package_name

        if not package:
            if cmd[0] == 'exec':
                p = subprocess.Popen(cmd[1], stdout=subprocess.PIPE, universal_newlines=True)
                self.process = p
            else:
                raise CommandNotRecognized
        else:
            if cmd[0] == 'docker':
                image_path = os.path.join(BASE_PATH, package_name, cmd[1])
                load_command = ['docker', 'load', image_path]
                docker_load = subprocess.Popen(load_command, stdout=subprocess.PIPE, universal_newlines=True)
                returncode = p.wait()
                if not returncode == 0:
                    command = ['docker', 'run', cmd[2]]
                    for arg in cmd[3]:
                        run_command.append(arg)
                    p = subprocess.Popen(run_command, stdout=subprocess.PIPE, universal_newlines=True)
                    self.process = p
            else:
                raise CommandNotRecongized

        t = Thread(target=reader,args=(p.stdout,self.linebuffer))
        t.daemon=True
        t.start()
        self.thread = t

    def ReInit(self, cmd):
        self.cmd = cmd
        package = self.package
        package_name = self.package_name

        if not package:
            if cmd[0] == 'exec':
                p = subprocess.Popen(cmd[1], stdout=subprocess.PIPE, universal_newlines=True)
                self.process = p
            else:
                raise CommandNotRecognized
        else:
            if cmd[0] == 'docker':
                image_path = os.path.join(BASE_PATH, package_name, cmd[1])
                load_command = ['docker', 'load', image_path]
                docker_load = subprocess.Popen(load_command, stdout=subprocess.PIPE, universal_newlines=True)
                returncode = p.wait()
                if not returncode == 0:
                    command = ['docker', 'run', cmd[2]]
                    for arg in cmd[3]:
                        run_command.append(arg)
                    p = subprocess.Popen(run_command, stdout=subprocess.PIPE, universal_newlines=True)
                    self.process = p
            else:
                raise CommandNotRecongized

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
