import hashlib

class ProofOfWork:
    @staticmethod
    def mine_block(block, difficulty):
        while not ProofOfWork.is_valid_proof(block.hash, difficulty):
            block.nonce += 1
            block.calculate_hash()

    @staticmethod
    def is_valid_proof(block_hash, difficulty):
        return block_hash.startswith('0' * difficulty)
