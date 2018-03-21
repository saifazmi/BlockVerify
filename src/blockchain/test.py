from transaction import Transaction, TransactionPool
from block import Block
from blockchain import Blockchain


## Blockchain
chain = Blockchain()
print(repr(chain))
print(str(chain))

## Transactions
PY_ZEN_HASH = 'e250f274f33b9b621a04264025d50e5fb9b1f989f444d13bb373882e734e996f'
with open('./files/my_pgp_key.asc') as pub_key:
    AUTHOR_KEY = pub_key.read()
with open('./files/sign.asc') as sign:
    SIGNATURE = sign.read()

# genesis transaction
gen_txn = Transaction(PY_ZEN_HASH, AUTHOR_KEY, SIGNATURE)

# some dummy transactions
txn_pool = TransactionPool()
txn_pool.add_transaction(gen_txn)
txn_7 = None  # for verification testing
for i in range(1, 17):  # 16 + 1 transactions
    t = Transaction(
        'file_hash_{}'.format(i),
        'author_key_{}'.format(i),
        'signature_{}'.format(i))
    if i == 7:
        txn_7 = t
    txn_pool.add_transaction(t)

print('='*10)
print('Dummy Transaction Pool:')
print(txn_pool)

## Blocks
# genesis block
genesis = Block(0)

# some dummy transactions
blocks = [genesis]
for i in range(1, 5):  # 4 + 1 Blocks
    b = Block(i)
    blocks.append(b)

print('='*10)
print('Dummy Blocks:')
[print(blocks[i]) for i in range(len(blocks))]

# Build the blockchain with txns
print('='*10)
print('Adding transactions to blocks (4 txns/block)...')
# hard coding 1 genesis transaction
blocks[0].add_transaction(txn_pool.get_transaction())
for i in range(1, 5):
    for j in range(1, 5):
        blocks[i].add_transaction(txn_pool.get_transaction())

# Generating hash manually for now
blocks[0].set_block_hash(None)
blocks[1].set_block_hash(blocks[0])
blocks[2].set_block_hash(blocks[1])
blocks[3].set_block_hash(blocks[2])
blocks[4].set_block_hash(blocks[3])
print('Generating merkle root...')
[print(str(blocks[i].merkle_tree.get_merkle_root())) for i in range(len(blocks))]
print('Generating block hash...')
[print(blocks[i].block_hash) for i in range(len(blocks))]


print('Adding blocks to chain...')
[chain.accept_block(blocks[i]) for i in range(len(blocks))]
print('Verifying block chain...')
chain.verify_chain()

print('='*10)
print('Updating index of block #3...')
blocks[3].index = 8
print('Verifying again...')
chain.verify_chain()

print('='*10)
print('Updating file_hash in  txn #7 of block #2...')
blocks[3].index = 3  # resetting for txn test
txn_7.file_hash = 'beeboop'
print('Verifying again...')
chain.verify_chain()
