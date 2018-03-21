from block import GenesisBlock, Block
from transaction import Transaction


class Blockchain:

    def __init__(self):
        self.current_block = None  # tail of the chain
        self.genesis_block = None  # head of the chain
        self.blocks = []
        self.transaction_pool = []
        self._genesis()

    def __repr__(self):
        return 'Blockchain({})'.format(repr(self.genesis_block))

    def __str__(self):
        return 'Blockchain // genesis:{} / current:{} / total_blocks:{}' \
            .format(
                repr(self.genesis_block),
                repr(self.current_block),
                len(self.blocks))

    def add_transaction(self, data):
        txn = Transaction()
        txn.from_dict(data)
        self.transaction_pool.append(txn)

    def accept_block(self, block):
        if self.genesis_block is None:
            self.genesis_block = block
            self.genesis_block.previous_block_hash = None

        self.current_block = block
        self.blocks.append(block)

    def mine(self):
        block = Block(self.current_block.index + 1)
        for txn in self.transaction_pool:
            block.add_transaction(txn)

        block.set_block_hash(self.current_block)
        self.accept_block(block)
        return block.index

    def file_exists(self, file_hash):
        exists = False

        # check the txns in blocks for file hash
        for block in self.blocks:
            for txn in block.transactions:
                if txn.file_hash == file_hash:
                    exists = True

        # check the txns in txn pool for file hash
        for txn in self.transaction_pool:
            if txn.file_hash == file_hash:
                    exists = True

        return exists

    def verify_chain(self):
        if self.genesis_block is None:
            raise Exception('Genesis block not defined')

        is_valid = self.genesis_block.is_valid_chain(None)

        if is_valid:
            print('Blockchain integrity intact.')
        else:
            print('Blockchain integrity compromised!')

        return is_valid

    def _genesis(self):
        block = GenesisBlock()
        self.accept_block(block)

    def to_dict(self, blocks=False, txns=False):
        data = {
            'current_block': self.current_block.block_hash,
            'genesis_block': self.genesis_block.block_hash,
            'total_blocks': len(self.blocks),
        }
        if blocks:
            data['blocks'] = [block.to_dict(txns) for block in self.blocks]
        return data
