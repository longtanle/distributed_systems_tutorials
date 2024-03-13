# echo-server.py

import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

try:
    # Create a socket object using a context manager for automatic cleanup
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
       
        # Bind the socket to the specified host and port
        print("Server host names: ", HOST, "Port: ", PORT)
        s.bind((HOST, PORT))
        # Start listening for incoming connections
        s.listen(0)
        print("Listening...")

        # Server main loop
        while True:
            # Accept a new connection
            conn, addr = s.accept()
            # Use a context manager to automatically close the connection
            with conn:
                print(f"Connected by {addr}")
                # Inner loop for receiving messages from a client
                while True:
                    # Receive data from the client, buffer size is 1024 bytes
                    data = conn.recv(1024)
                    # If no data is received, this means the client has closed the connection
                    if not data:
                        break  # Exit the inner loop
                    # Echo the received data back to the client
                    conn.sendall(data)
                # After the inner loop is exited, the connection is closed automatically
                print(f"Connection with {addr} closed.")
except:
    # If an exception occurs, print error message
    print("Can't connect to the Socket")  