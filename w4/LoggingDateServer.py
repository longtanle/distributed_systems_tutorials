import threading
import time
import datetime
import socket
HOST = "127.0.0.1"
PORT_Server = 6015
class LoggingDateServer():
    def __init__(self, *args):
        self.args = args

    def store(self, time, id, addr):
        filename = "log" + str(id) + ".txt"
        with open(filename, 'a') as out:
            out.write(time + ": received from " + str(addr) + '\n')

    def run(self):
        id = 0
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                #s = socket.socket()
                #host = socket.gethostname() # Get local machine name   
                print("Server host names: ", HOST, "Port: ",PORT_Server)
                s.bind((HOST, PORT_Server))        # Bind to the port
                s.listen() 
                while(1):
                    c, addr = s.accept()     # Establish connection with client.
                    id += 1
                    print("Got connection from", addr)
                    data_rev = c.recv(1024)
                    if not data_rev:
                        print("didn't get data")
                        break
                    print(str(addr) + " Client " + str(id) + ": " + data_rev.decode('utf-8'))
                    time =  datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
                    self.store(time ,id , addr)
                    data = bytes(time, encoding= 'utf-8')
                    c.sendall(data)
                    c.close()       
        except:
            print("Can't connect to the Socket")

server = LoggingDateServer()
server.run()