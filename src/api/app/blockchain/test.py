from transaction import Transaction, TransactionPool
from block import Block
from blockchain import Blockchain


# Blockchain
chain = Blockchain()
print(repr(chain))
print(str(chain))

# Transactions
# some dummy transactions
txn_pool = TransactionPool()
txn_10 = None  # for verification testing
for i in range(1, 17):  # 16  transactions
    t = Transaction(
        'file_hash_{}'.format(i),
        'author_key_{}'.format(i),
        'signature_{}'.format(i))
    if i == 10:
        txn_10 = t
    txn_pool.add_transaction(t)

print('='*10)
print('Dummy Transaction Pool:')
print(txn_pool)

# Blocks
# some dummy blocks
blocks = []
for i in range(1, 5):  # 4
    b = Block(i)
    blocks.append(b)

print('='*10)
print('Dummy Blocks:')
[print(blocks[i]) for i in range(len(blocks))]
print('TOTAL Blocks = {}'.format(len(blocks)))

# Build the blockchain with txns
print('='*10)
print('Adding transactions to blocks (4 txns/block)...')
for i in range(len(blocks)):
    for j in range(4):
        blocks[i].add_transaction(txn_pool.get_transaction())

# Generating hash manually for now
blocks[0].set_block_hash(chain.genesis_block)
blocks[1].set_block_hash(blocks[0])
blocks[2].set_block_hash(blocks[1])
blocks[3].set_block_hash(blocks[2])
[chain.accept_block(blocks[i]) for i in range(len(blocks))]
print('Generating merkle root...')
[print(str(chain.blocks[i].merkle_tree.get_merkle_root()))
    for i in range(len(chain.blocks))]
print('Generating block hash and PoW...')
[print('{}::{}'.format(chain.blocks[i].nonce, chain.blocks[i].block_hash))
    for i in range(len(chain.blocks))]

print('='*10)
print('Adding blocks to chain...')
print(repr(chain))
print(str(chain))

print('='*10)
print('Verifying block chain...')
chain.verify_chain()

print('='*10)
print('Updating index of block #2...')
chain.blocks[2].index = 8
print('Verifying again...')
chain.verify_chain()

print('='*10)
print('Updating file_hash in  txn #10 of block #3...')
chain.blocks[2].index = 2  # resetting for txn test
txn_10.file_hash = 'beeboop'
print('Verifying again...')
chain.verify_chain()
