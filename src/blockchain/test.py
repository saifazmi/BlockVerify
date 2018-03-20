from time import time

from transaction import Transaction
from block import Block
from blockchain import Blockchain


## Blockchain
chain = Blockchain()
print(repr(chain))
print(str(chain))

## Transactions
PY_ZEN_HASH = 'e250f274f33b9b621a04264025d50e5fb9b1f989f444d13bb373882e734e996f'
with open('my_pgp_key.asc') as pub_key:
    AUTHOR_KEY = pub_key.read()
with open('sign.asc') as sign:
    SIGNATURE = sign.read()

# genesis transaction
gen_txn = Transaction(PY_ZEN_HASH, AUTHOR_KEY, SIGNATURE)

# some dummy transactions
txns = [gen_txn]
for i in range(1, 17): # 16 + 1 transactions
    t = Transaction(
        'file_hash_{}'.format(i),
        'author_key_{}'.format(i),
        'signature_{}'.format(i))
    txns.append(t)

print('='*10)
print('Dummy Transactions:')
[print(txns[i]) for i in range(len(txns))]

## Blocks
# genesis block
genesis = Block(0)

# some dummy transactions
blocks = [genesis]
for i in range(1, 5): # 4 + 1 Blocks
    b = Block(i)
    blocks.append(b)

print('='*10)
print('Dummy Blocks:')
[print(blocks[i]) for i in range(len(blocks))]

## Build the blockchain with txns
print('='*10)
print('Adding transactions to blocks (4 txns/block)...')
blocks[0].add_transaction(txns[0])  # hard coding 1 genesis transaction

blocks[1].add_transaction(txns[1])
blocks[1].add_transaction(txns[2])
blocks[1].add_transaction(txns[3])
blocks[1].add_transaction(txns[4])

blocks[2].add_transaction(txns[5])
blocks[2].add_transaction(txns[6])
blocks[2].add_transaction(txns[7])
blocks[2].add_transaction(txns[8])

blocks[3].add_transaction(txns[9])
blocks[3].add_transaction(txns[10])
blocks[3].add_transaction(txns[11])
blocks[3].add_transaction(txns[12])

blocks[4].add_transaction(txns[13])
blocks[4].add_transaction(txns[14])
blocks[4].add_transaction(txns[15])
blocks[4].add_transaction(txns[16])

# Generating hash manually for now
print('Generating block hash...')
blocks[0]._set_block_hash(None)
blocks[1]._set_block_hash(blocks[0])
blocks[2]._set_block_hash(blocks[1])
blocks[3]._set_block_hash(blocks[2])
blocks[4]._set_block_hash(blocks[3])
[print(blocks[i].block_hash) for i in range(len(blocks))]
print('Generating merkle root...')
[print(str(blocks[i].merkle_tree.get_merkle_root())) for i in range(len(blocks))]


print('Adding blocks to chain...')
[chain.accept_block(blocks[i]) for i in range(len(blocks))]
print('Verifying block chain...')
chain.verify_chain()

# print('='*10)
# print('Updating timestamp of block #2...')
# blocks[2].timestamp = time()
# print('Verifying again...')
# chain.verify_chain()

print('='*10)
print('Updating file_hash in  txn #7 of block #2...')
txns[7].file_hash = 'beeboop'
print('Verifying again...')
chain.verify_chain()
