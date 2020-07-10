import datetime
import hashlib


class Block:

    def __init__(self, tx):
        self.transactions = tx
        self.next = None
        self.blockNo = 0
        self.nonce = 0
        self.previous_hash = 0x0
        self.timestamp = datetime.datetime.now()
        self.hash = self.hash

    def hash(self):
        h = hashlib.sha256()
        h.update(
            str(self.nonce).encode('utf-8') +
            str(self.transactions).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.timestamp).encode('utf-8')
        )
        return h.hexdigest()


class Blockchain:
    diff = 5
    maxNonce = 2 ** 32
    target = 2 ** (256 - diff)
    blocks = [Block(["Genesis, 0"])]

    def add(self, block):
        top_block = self.blocks[-1]
        top_block.next = block

        block.previous_hash = top_block.hash()
        block.blockNo = top_block.blockNo + 1

        self.blocks.append(block)

    def mine(self, block):
        for i in range(500000000):
            if int(block.hash(), 16) > self.target:
                block.nonce += 1
            else:
                block.hash = block.hash
                self.add(block)
                break
