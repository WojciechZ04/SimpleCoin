import hashlib
import time

class Block:
    def __init__(self, index, transactions, prev_hash, timestamp=None, nonce=0):
        self.index = index
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.timestamp = timestamp or time.time()
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.transactions}{self.prev_hash}{self.timestamp}{self.nonce}"
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()
