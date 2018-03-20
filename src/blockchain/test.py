from block import Block
from blockchain import Blockchain


# blockchain
chain = Blockchain()

# genesis block
genesis = Block(0, None, 'file_hash_0', 'author_key-0', 'signature_0')

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

# [print(blocks[i]) for i in range(len(blocks))]

[chain.accept_block(blocks[i]) for i in range(len(blocks))]
chain.verify_chain()
