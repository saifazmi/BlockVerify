class Blockchain:

    def __init__(self):
        self.current_block = None
        self.genesis_block = None  # head of the chain
        self.blocks = []

    def __repr__(self):
        return 'Blockchain({})'.format(self.genesis_block)

    def __str__(self):
        return 'Blockchain // genesis:{} / current:{} / total_blocks:{}'.format(
            self.genesis_block, self.current_block, len(self.blocks)
        )

    def accept_block(self, block):
        if self.genesis_block is None:
            self.genesis_block = block
            self.genesis_block.previous_block_hash = None

        self.current_block = block
        self.blocks.append(block)

    def verify_chain(self):
        if self.genesis_block is None:
            print('Genesis block not set.')

        is_valid = self.genesis_block.is_valid_chain(None)

        if is_valid:
            print('Blockchain integrity intact.')
        else:
            print('Blockchain integrity compromised!')
