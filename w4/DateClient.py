import threading
import time
import socket
HOST = "127.0.0.1"
PORT_Server = 6015

class DateClient():
    def __init__(self, *args):
        self.args = args     
    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT_Server))
                s.sendall(b'Hello, what time is it?')
                data_rev = s.recv(1024)
                print(data_rev.decode('utf-8'))
                s.close()   
        except:
            print("Can't connect to the Socket")

client = DateClient()
client.run()