import cryptography.hazmat.primitives.asymmetric.ed25519 as ed25519
import socket

from blockchain import make_signature, make_transaction
from network import recv_prefixed, send_prefixed

# TODO generate a private key and create a transaction using make_signature and make_transaction
# using the derived public key as the sender

# TODO create a socket and connect to the blockchain node

# TODO send the transaction, receive the response and print it
