from block import GenesisBlock
from transaction import TransactionPool


class Blockchain:

    def __init__(self):
        self.current_block = None  # tail of the chain
        self.genesis_block = None  # head of the chain
        self.blocks = []
        self.transaction_pool = TransactionPool()
        self._genesis()

    def __repr__(self):
        return 'Blockchain({})'.format(repr(self.genesis_block))

    def __str__(self):
        return 'Blockchain // genesis:{} / current:{} / total_blocks:{}' \
            .format(
                repr(self.genesis_block),
                repr(self.current_block),
                len(self.blocks))

    def accept_block(self, block):
        if self.genesis_block is None:
            self.genesis_block = block
            self.genesis_block.previous_block_hash = None

        self.current_block = block
        self.blocks.append(block)

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
            'total_blocks': len(self.blocks)
        }
        if blocks:
            data['blocks'] = [block.to_dict(txns) for block in self.blocks]
        return data
