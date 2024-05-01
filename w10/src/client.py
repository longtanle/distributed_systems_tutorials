import cryptography.hazmat.primitives.asymmetric.ed25519 as ed25519
import socket

from blockchain import make_signature, make_transaction
from network import recv_prefixed, send_prefixed

print("Generating Transaction....\n")

private_key = ed25519.Ed25519PrivateKey.generate()
sender = private_key.public_key().public_bytes_raw().hex()
message = 'hello'
signature = make_signature(private_key, message)
transaction = make_transaction(sender, message, signature)

print(transaction)

print("\nSending Transaction....\n")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 8000))

send_prefixed(s, transaction.encode())
try:
	data = recv_prefixed(s).decode()
	print(data)
except Exception as e:
	print(e)
