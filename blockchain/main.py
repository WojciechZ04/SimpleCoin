from blockchain import Blockchain
from block import Block
from transaction import Transaction
from proofOfWork import ProofOfWork

# Inicjalizacja blockchaina
blockchain = Blockchain()

# Dodanie kilku bloków i transakcji do blockchaina (przykładowe dane)
transaction1 = Transaction("Alice", "Bob", 10)
block1 = Block(1, [transaction1], blockchain.get_latest_block().hash)
ProofOfWork.mine_block(block1, 2)
blockchain.add_block(block1)

transaction2 = Transaction("Bob", "Charlie", 5)
block2 = Block(2, [transaction2], blockchain.get_latest_block().hash)
ProofOfWork.mine_block(block2, 2)
blockchain.add_block(block2)

print("test")
# Wyświetlenie łańcucha bloków
for block in blockchain.chain:
    print(f"Block {block.index} - Hash: {block.hash}")
    for transaction in block.transactions:
        print(f"   Transaction: {transaction.sender} -> {transaction.recipient}: {transaction.amount}")

input("Naciśnij Enter, aby zakończyć...")
