from argparse import ArgumentParser
import json
from threading import Lock
import socketserver

from blockchain import Blockchain
from network import recv_prefixed, send_prefixed

class MyTCPServer(socketserver.ThreadingTCPServer):
	def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
		# TODO initialize self.blockchain and self.blockchain_lock
		super().__init__(server_address, RequestHandlerClass, bind_and_activate)

class MyTCPHandler(socketserver.BaseRequestHandler):
	server: MyTCPServer

	def handle(self):
		# TODO create an infinite loop with the following steps
		# 1. receive data from the client using recv_prefixed and self.request
		# break to exit the loop in case of exception
		# 2. print the received data
		# 3. add the transaction to blockchain. use self.blockchain_lock to avoid data race
		# 4. send the response to the client using send_prefixed
		pass

if __name__ == '__main__':
	# TODO setup ArgumentParser with a required port argument of type int

	HOST = 'localhost'

	# TODO create an instance of MyTCPServer with the host, port, and MyTCPHandler
	# and use serve_forever to serve the requests. This will keep running until you
	# interrupt the program with Ctrl-C
