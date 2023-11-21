import json
from block import Block
received_json = '{"hash": "abc123", "prev_hash": "def456", "nonce": 123, "data": "Some data"}' # Przyktadowy JSON
received_dict = json.loads(received_json)



received_block = Block(data=received_dict["data"],prev_hash=bytes.fromhex(received_dict["prev_hash"]), nonce=received_dict["nonce"])


print(received_block)