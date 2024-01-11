import hashlib
from datetime import datetime
import json

class Block:
    def __init__(self, index, hash, previous_hash, timestamp, data, nonce, difficulty):
        self.index = index
        self.hash = hash
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.difficulty = difficulty

    def to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)



def calculate_hash(index, previous_hash, timestamp, data, diffilcuty, nonce):
    string_to_hash = str(index) + str(previous_hash) + str(timestamp) + data +str(diffilcuty) + str(nonce)
    hashed = hashlib.sha256(string_to_hash.encode()).hexdigest()
    return hashed




def generate_next_block(block_data,blockchain,difficulty):
    previous_block = blockchain[-1]
    # print('Difficulty: ' + str(difficulty))
    next_index = previous_block.index + 1
    next_timestamp = datetime.now().timestamp()
    new_block = find_block(next_index, previous_block.hash, next_timestamp, block_data, difficulty)
    return new_block

def is_valid_new_block(new_block, previous_block):
    if previous_block.index + 1 != new_block.index:
        print('invalid index')
        return False
    elif previous_block.hash != new_block.previous_hash:
        # print('invalid previoushash')
        return False
    elif calculate_hash(new_block.index, new_block.previous_hash, new_block.timestamp, new_block.data, new_block.difficulty, new_block.nonce) != new_block.hash:
        print(type(new_block.hash), type(calculate_hash(new_block)))
        print(f'invalid hash: {calculate_hash(new_block)} {new_block.hash}')
        return False
    return True


def is_valid_chain(blockchain_to_validate, genesis_block):
    def is_valid_genesis(block):
        return block.__dict__ == genesis_block.__dict__
    if not is_valid_genesis(blockchain_to_validate[0]):
        return False
    for i in range(1, len(blockchain_to_validate)):
        if not is_valid_new_block(blockchain_to_validate[i], blockchain_to_validate[i - 1]):
            return False
    return True

def find_block(index, previous_hash, timestamp, data, difficulty):
    nonce = 0
    while True:
        block = Block(index, '', previous_hash, timestamp, data, nonce, difficulty)
        block_hash = calculate_hash(index, previous_hash, timestamp, data, difficulty, nonce)
        if block_hash.startswith('0' * difficulty):
            block.hash = block_hash
            return block
        nonce += 1


bG = Block(index=0, previous_hash= 'P15n2b085vhh0235vh21v8508123v08g2v0', hash = None,timestamp='20231227', data='Genesis block',nonce=10, difficulty=1)
print(bG.to_json())
# blockchain = [bG]
# #
# b1 = generate_next_block('BLOK1', blockchain, 2)
#
# spr = is_valid_new_block(b1,bG)
# # print(spr)
# spr_ch = is_valid_chain(blockchain,bG)
# # print(spr_ch)
# blockchain.append(b1)
# #
# b2 = generate_next_block('BLOK2',blockchain, 2)
# spr = is_valid_new_block(b2,b1)
# # print(spr)
# spr_ch = is_valid_chain(blockchain,bG)
# # print(spr_ch)
# blockchain.append(b2)
#
# print("ZMIANA TRUDNOSCI")
#
#
# bG = Block(index=0, previous_hash= 'P15n2b085vhh0235vh21v8508123v08g2v0', hash = None,timestamp='20231227', data='Genesis block',nonce=10, difficulty=4)
# blockchain4 = [bG]
#
# #
# b14 = generate_next_block('BLOK14', blockchain4, 4)
#
# spr = is_valid_new_block(b14,bG)
# print(spr)
# spr_ch = is_valid_chain(blockchain4,bG)
# print(spr_ch)
# blockchain4.append(b14)
# #
# b24 = generate_next_block('BLOK24', blockchain4,4 )
#
# spr = is_valid_new_block(b24,b14)
# print(spr)
# spr_ch = is_valid_chain(blockchain4,bG)
# print(spr_ch)
# blockchain4.append(b24)

#
def choose_blockchain_diffi(bc1,bc2):
    d_bc1 = 0
    for ele in bc1:
        d_bc1 += ele.difficulty
    d_bc2 = 0
    for ele in bc2:
        d_bc2 += ele.difficulty
    if d_bc1 > d_bc2:
        print('Wybrano łańcuch 1')
    else:
        print('Wybrano łańcuch 2')

# choose_blockchain_diffi(blockchain, blockchain4)

def choose_blockchain_ts(bc1,bc2):
    ts_bc1 = 0
    for ele in bc1:
        ts_bc1 += ele.timestamp
    ts_bc2 = 0
    for ele in bc2:
        ts_bc2 += ele.timestamp
    if ts_bc1 < ts_bc2:
        print('Wybrano łańcuch 1')
    else:
        print('Wybrano łańcuch 2')



# choose_blockchain_diffi(blockchain, blockchain4)



