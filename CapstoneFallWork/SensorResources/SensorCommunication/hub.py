import socket, time, hashlib
from threading import Thread

HOST = "192.168.1.39"
PORT = 5454
PORT2 = 5555

#Wifi connect per node...will be different post Zigbee
pi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pi.bind((HOST, PORT))
pi.listen(1)

#"" ""
pi2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pi2.bind((HOST, PORT2))
pi2.listen(1)

conn, addr = s.accept()
print("Connection here: ", addr)
conn2, addr2 = s.accept()
print("Connection here also: ", addr2)

#Used to thread coordinate multi node queueing
class SensorMonitor(Thread):
        def __init__(self, conn):
                Thread.__init__(self)
                self.data = None
                self.last_data_hash = None
                self.conn = conn
        def update(self):
                newData = self.conn.recv(1024)
                hash = hashlib.sha1(newData)
                if hash != self.last_data_hash:
                        self.data = newData
                        text = newData.strip().decode('utf-8')
                        print("Message recieved: " + text)
        def run(self):
                while True:
                        self.update()

if conn != None and conn2 != None:
     s1 = SensorMonitor(conn)
     s2 = SensorMonitor(conn2)

     s1.start()
     s2.start()
