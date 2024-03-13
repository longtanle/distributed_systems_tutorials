# Import necessary modules
import threading  # For creating threads, not used in this code snippet
import time  # For handling time-related tasks, not used in this code snippet
import datetime  # For retrieving and formatting the current date and time
import socket  # For socket programming, enabling communication over the network

# Server configuration
HOST = "127.0.0.1"  # Loopback address for localhost
PORT_Server = 6015  # Arbitrary non-privileged port to listen on

# Define a class for the Date Server
class DateServer():
    def __init__(self, *args):
        self.args = args  # Allow passing arbitrary arguments, not utilized in this snippet

    # Method to run the server
    def run(self):
        try:
            # Create a socket object using context manager for automatic cleanup
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print("Server host names: ", HOST, "Port: ", PORT_Server)
                s.bind((HOST, PORT_Server))  # Bind the socket to the specified host and port
                s.listen(5)  # Listen for incoming connections, max 5 queued connections

                # Infinite loop to keep the server running
                while True:
                    c, addr = s.accept()  # Accept a connection, c is a new socket object for communication
                    print("Got connection from", addr)  # Print the address of the connected client

                    data_rev = c.recv(1024)  # Receive data from the client, buffer size is 1024 bytes
                    if not data_rev:
                        print("didn't get data")  # If no data is received, print message and break loop
                        break
                    print(data_rev.decode('utf-8'))  # Print received data after decoding it

                    # Get the current time and format it
                    time = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
                    # Convert the formatted time string to bytes
                    data = bytes(time, encoding='utf-8')  

                    print(time)  # Print the formatted time on the server side
                    c.sendall(data)  # Send the time data back to the client
                    c.close()  # Close the client socket
        except:
            print("Can't connect to the Socket")  # If an exception occurs, print error message

# Instantiate the DateServer class
server = DateServer()
# Run the server
server.run()
