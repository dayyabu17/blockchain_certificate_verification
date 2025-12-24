import hashlib
import json
from datetime import datetime


class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = str(datetime.utcnow())
        self.data = data                        # certificate + student info
        self.previous_hash = previous_hash      # hash of previous block
        self.hash = self.compute_hash()         # current block hash

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    # ---- GENESIS BLOCK ----
    def create_genesis_block(self):
        genesis_data = {"message": "Genesis Block"}
        genesis_block = Block(0, genesis_data, "0")
        self.chain.append(genesis_block)

    # ---- GET LAST BLOCK HASH ----
    def get_last_hash(self):
        return self.chain[-1].hash

    # ---- ADD NEW BLOCK ----
    def add_block(self, data):
        previous_hash = self.get_last_hash()
        index = len(self.chain)

        new_block = Block(index, data, previous_hash)
        self.chain.append(new_block)

        return index  # return block index to store in database

    # ---- VERIFY CHAIN INTEGRITY ----
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # If hash has been tampered
            if current.previous_hash != previous.hash:
                return False

            # If block was re-edited
            if current.hash != current.compute_hash():
                return False

        return True
