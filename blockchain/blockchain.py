import hashlib
import time

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, hash, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.hash = hash
        self.nonce = nonce

def calculate_hash(index, previous_hash, timestamp, transactions, nonce):
    value = str(index) + str(previous_hash) + str(timestamp) + str(transactions) + str(nonce)
    return hashlib.sha256(value.encode()).hexdigest()

def mine_block(index, previous_hash, timestamp, transactions, difficulty):
    nonce = 0
    while True:
        hash_attempt = calculate_hash(index, previous_hash, timestamp, transactions, nonce)
        if hash_attempt.startswith('0' * difficulty):
            return Block(index, previous_hash, timestamp, transactions, hash_attempt, nonce)
        nonce += 1

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty

    def add_block(self, transactions):
        if not self.chain:
            # Genesis block
            block = mine_block(0, '0', time.time(), transactions, self.difficulty)
        else:
            previous_block = self.chain[-1]
            block = mine_block(len(self.chain), previous_block.hash, time.time(), transactions, self.difficulty)
        self.chain.append(block)

# Utworzenie blockchaina i dodanie pierwszego bloku z coinbase transaction
blockchain = Blockchain()

# Coinbase transaction (pierwsza transakcja w blockchainie)
coinbase_transaction = Transaction("coinbase", "miner_address", 50)
genesis_transactions = [coinbase_transaction]

# Dodanie pierwszego bloku z coinbase transaction
blockchain.add_block(genesis_transactions)

# Wyświetlenie informacji o pierwszym bloku w blockchainie
first_block = blockchain.chain[0]
print(f"Block {first_block.index} - Hash: {first_block.hash}")
print(f"   Previous Hash: {first_block.previous_hash}")
print(f"   Timestamp: {first_block.timestamp}")
print(f"   Transactions: {first_block.transactions[0].amount} coins mined")
print(f"   Nonce: {first_block.nonce}")
print("\n")
