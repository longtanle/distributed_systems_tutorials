import socket
import struct

def recv_exact(sock: socket.socket, msglen):
	chunks = []
	bytes_recd = 0
	while bytes_recd < msglen:
		chunk = sock.recv(min(msglen - bytes_recd, 2048))
		if chunk == b'':
			raise RuntimeError("socket connection broken")
		chunks.append(chunk)
		bytes_recd = bytes_recd + len(chunk)
	return b''.join(chunks)

def send_exact(sock: socket.socket, msg: bytes):
	totalsent = 0
	while totalsent < len(msg):
		sent = sock.send(msg[totalsent:])
		if sent == 0:
			raise RuntimeError("socket connection broken")
		totalsent = totalsent + sent

def recv_prefixed(sock: socket.socket):
	size_bytes = recv_exact(sock, 2)
	size = struct.unpack("!H", size_bytes)[0]
	if size == 0:
		raise RuntimeError("empty message")
	if size > 65535 - 2:
		raise RuntimeError("message too large")
	return recv_exact(sock, size)

def send_prefixed(sock: socket.socket, msg: bytes):
	size = len(msg)
	if size == 0:
		raise RuntimeError("empty message")
	if size > 65535 - 2:
		raise RuntimeError("message too large")
	size_bytes = struct.pack("!H", size)
	send_exact(sock, size_bytes + msg)
