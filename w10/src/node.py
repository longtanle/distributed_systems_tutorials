from argparse import ArgumentParser
import json
from threading import Lock
import socketserver

from blockchain import Blockchain
from network import recv_prefixed, send_prefixed

class MyTCPServer(socketserver.ThreadingTCPServer):
	def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
		self.blockchain = Blockchain()
		self.blockchain_lock = Lock()
		super().__init__(server_address, RequestHandlerClass, bind_and_activate)

class MyTCPHandler(socketserver.BaseRequestHandler):
	server: MyTCPServer

	def handle(self):
		while True:
			try:
				data = recv_prefixed(self.request).decode()
			except:
				break
			print("Received from {}:".format(self.client_address[0]))
			print(data)
			with self.server.blockchain_lock:
				added = self.server.blockchain.add_transaction(data)
			send_prefixed(self.request, json.dumps({'response': added}).encode())

if __name__ == '__main__':
	parser = ArgumentParser()
	parser.add_argument('port', type=int)
	args = parser.parse_args()
	port: int = args.port

	HOST = 'localhost'

	with MyTCPServer((HOST, port), MyTCPHandler) as server:
		server.serve_forever()
