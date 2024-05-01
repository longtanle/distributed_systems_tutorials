from cryptography.exceptions import InvalidSignature
import cryptography.hazmat.primitives.asymmetric.ed25519 as ed25519
from enum import Enum
import hashlib
import json
import re

sender_valid = re.compile('^[a-fA-F0-9]{64}$')
signature_valid = re.compile('^[a-fA-F0-9]{128}$')

TransactionValidationError = Enum('TransactionValidationError', ['INVALID_JSON', 'INVALID_SENDER', 'INVALID_MESSAGE', 'INVALID_SIGNATURE'])

def make_transaction(sender, message, signature) -> str:
	return json.dumps({'sender': sender, 'message': message, 'signature': signature})

def transaction_bytes(transaction: dict) -> bytes:
	return json.dumps({k: transaction.get(k) for k in ['sender', 'message']}, sort_keys=True).encode()

def make_signature(private_key: ed25519.Ed25519PrivateKey, message: str) -> str:
	transaction = {'sender': private_key.public_key().public_bytes_raw().hex(), 'message': message}
	return private_key.sign(transaction_bytes(transaction)).hex()

def validate_transaction(transaction: str) -> dict | TransactionValidationError:
	try:
		tx = json.loads(transaction)
	except json.JSONDecodeError:
		return TransactionValidationError.INVALID_JSON

	if not(tx.get('sender') and isinstance(tx['sender'], str) and sender_valid.search(tx['sender'])):
		return TransactionValidationError.INVALID_SENDER

	if not(tx.get('message') and isinstance(tx['message'], str) and len(tx['message']) <= 70 and tx['message'].isalnum()):
		return TransactionValidationError.INVALID_MESSAGE

	public_key = ed25519.Ed25519PublicKey.from_public_bytes(bytes.fromhex(tx['sender']))
	if not(tx.get('signature') and isinstance(tx['signature'], str) and signature_valid.search(tx['signature'])):
		return TransactionValidationError.INVALID_SIGNATURE
	try:
		public_key.verify(bytes.fromhex(tx['signature']), transaction_bytes(tx))
	except InvalidSignature:
		return TransactionValidationError.INVALID_SIGNATURE

	return tx


class Blockchain():
	def  __init__(self):
		self.blockchain = []
		self.pool = []
		self.new_block('0' * 64)

	def new_block(self, previous_hash=None):
		block = {
			'index': len(self.blockchain) + 1,
			'transactions': self.pool.copy(),
			'previous_hash': previous_hash or self.blockchain[-1]['current_hash'],
		}
		block['current_hash'] = self.calculate_hash(block)
		self.pool = []
		self.blockchain.append(block)

	def last_block(self):
		return self.blockchain[-1]

	def calculate_hash(self, block: dict) -> str:
		block_object: str = json.dumps({k: block.get(k) for k in ['index', 'transactions', 'previous_hash']}, sort_keys=True)
		block_string = block_object.encode()
		raw_hash = hashlib.sha256(block_string)
		hex_hash = raw_hash.hexdigest()
		return hex_hash

	def add_transaction(self, transaction: str) -> bool:
		if isinstance((tx := validate_transaction(transaction)), dict):
			self.pool.append(tx)
			return True
		return False
