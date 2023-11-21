import hashlib
import json
class Block:
    def __init__(self, data, prev_hash, nonce):
        self.hash = hashlib.sha256()
        self.prev_hash = prev_hash
        self.nonce = nonce
        self.data = data

    def mine(self, difficulty):
        self.hash.update(str(self).encode('utf-8'))
        while int(self.hash.hexdigest(), 16) > 2 ** (256 - difficulty):
            self.nonce += 1
            print(self.nonce)
            self.hash = hashlib.sha256()
            self.hash.update(str(self).encode('utf-8'))

    def to_dict_nonce(self):
        return self.nonce
    def to_dict_prev_hash(self):
        return self.prev_hash.hexdigest()
    def to_dict_data(self):
        return self.data


    def to_json_nonce(self):
        block_dict = self.to_dict_nonce()
        return json.dumps(block_dict)
    def to_json_prev_hash(self):
        block_dict = self.to_dict_prev_hash()
        return json.dumps(block_dict)
    def to_json_data(self):
        block_dict = self.to_dict_data()
        return json.dumps(block_dict)



    def __str__(self):
        print(self.prev_hash, 'samo self prevhasz')
        print(self.data)
        print(self.nonce)
        return f"{self.prev_hash.hexdigest()}{self.data}{self.nonce}"


