from time import time

from block import Block
from blockchain import Blockchain


# blockchain
chain = Blockchain()
print(repr(chain))
print(str(chain))

# genesis block
genesis = Block(0, None, 'file_hash_0', 'author_key-0', 'signature_0')
print(repr(genesis))
print(str(genesis))

# regular blocks
blocks = [genesis]
for i in range(1, 10):
    b = Block(
        i,
        blocks[i - 1],
        'file_hash_{}'.format(i),
        'author_key-{}'.format(i),
        'signature_{}'.format(i))
    blocks.append(b)

print('='*10)
print('Dummy Blocks:')
[print(blocks[i]) for i in range(len(blocks))]

print('='*10)
print('Adding blocks to chain...')
[chain.accept_block(blocks[i]) for i in range(len(blocks))]
print('Verifying block chain...')
chain.verify_chain()

print('='*10)
print('Updating timestamp of block #4...')
blocks[4].timestamp = time()
print('Verifying again')
chain.verify_chain()
