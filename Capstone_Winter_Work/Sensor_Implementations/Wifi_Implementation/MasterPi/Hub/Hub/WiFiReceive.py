import socket, time, hashlib, random, sys, queue
from time import sleep
from threading import Thread

HOST = "192.168.1.40"
PORT = 5454

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

class SensorMonitor(Thread):

        def __init__(self, bucket):
                Thread.__init__(self)
                self.data = None
                self.last_data_hash = None
                conn, addr = self.socketConnect()
                self.conn = conn
                self.bucket = bucket

        def socketConnect(self):
                conn, addr = server.accept()
                print("Connection here: ", addr)
                return conn, addr

        def update(self):
                newData = self.conn.recv(1024)
                hash = hashlib.sha1(newData)
                if hash != self.last_data_hash:
                        self.data = newData
                        try:
                                text = newData.strip().decode('utf-8')
                                print(text)
                                return text
                        except Exception:
                                self.bucket.put(sys.exc_info())

        def run(self):
                while True:
                        try:
                                #print(test) #The fuck is this doing?
                                test = self.update()
                                if test == None:
                                        self.conn.close()
                                        break
                        except: #(socket.error, KeyboardInterrupt) as e:
                                self.conn.shutdown(2)
                                self.conn.close()
                                print("FIRST")
                                break
bucket = queue.Queue()

while True:
        device = SensorMonitor(bucket)
        device.start()

        try:
                exc = bucket.get(block=False)
        except queue.Empty:
                pass
        else:
                exc_type, exc_obj, exc_trace = exc
                print(exc_type)
                print(exc_obj)
                print(exc_trace)

        device.join(0.1)
        if device.isAlive():
                continue
        else:
                break


