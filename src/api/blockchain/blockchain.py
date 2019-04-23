from block import GenesisBlock, Block
from transaction import Transaction


class Blockchain:
    """
    A class used to represent a collection of blocks forming a Blockchain.

    Attributes
    ----------
    current_block : Block
        The last block or tail of the blockchain
    genesis_block : Block
        The first block or head of the blockchain
    blocks : list
        List of all the blocks in this blockchain
    transaction_pool : list
        List of currently unprocessed transactions

    Methods
    -------
    add_transactions(data)
        Adds the given data as a transaction to the transaction pool
        of this blockchain.
    accept_block(block)
        Adds a block to the blockchain
    mine()
        Mines a block by processing the transaction pool and adds it
        to this blockchain.
    file_exists(file_hash)
        Checks if a file already exists in this blockchain.
    verify_chain
        Verifies the integrity (immutability) of this blockchain.
    _genesis()
        Iinitialises and adds the Genesis block to this blockchain.
    to_dict(blocks, txns)
        Converts this object to a python dicitonary.
    """

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

    def __len__(self):
        return len(self.blocks)

    def add_transaction(self, data):
        """Adds the given data as a transaction to the transaction pool
        of this blockchain.

        Parameters
        ----------
        data : dict
            The transaction data to be added to this blockchain
        """

        txn = Transaction()  # create new txn
        txn.from_dict(data)  # initialise with json data
        self.transaction_pool.append(txn)

    def accept_block(self, block):
        """Adds a block to the blockchain.

        Parameters
        ----------
        block : Block
            The block to be added to this blockchain
        """

        if self.genesis_block is None:
            self.genesis_block = block
            self.genesis_block.previous_block_hash = None

        self.current_block = block
        self.blocks.append(block)

    def mine(self):
        """Mines a block by processing the transaction pool and adds it
        to this blockchain.

        Returns
        -------
        int
            The index of the new block in this blockchain
        """

        block = Block(self.current_block.index + 1)
        for txn in self.transaction_pool:
            block.add_transaction(txn)

        block.set_block_hash(self.current_block)
        self.accept_block(block)
        self.transaction_pool.clear()
        return block.index

    def file_exists(self, file_hash):
        """Checks if a file already exists in this blockchain.

        Parameters
        ----------
        file_hash : str
            The SHA-256 hash of the file to be searched for

        Returns
        -------
        bool
            True if the file exists in this blockchain else False
        """

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
        """Verifies the integrity (immutability) of this blockchain.

        Raises
        ------
        Exception
            If the blockchain has not been initialised properly with a
            genesis block

        Returns
        -------
        bool
            True if the data in this blockchain has not been modified
            else False
        """

        if self.genesis_block is None:
            raise Exception('Genesis block not defined')

        is_valid = self.genesis_block.is_valid_chain()

        if is_valid:
            print('Blockchain integrity intact.')
        else:
            print('Blockchain integrity compromised!')

        return is_valid

    # Iinitialises and adds the Genesis block to this blockchain
    def _genesis(self):
        block = GenesisBlock()
        self.accept_block(block)

    def to_dict(self, blocks=False, txns=False):
        """Converts this object to a python dicitonary.

        Parameters
        ----------
        blocks : bool, optional
            set to True to include all the blocks in this blockchain
            (the default is False, which doesn't include blocks)
        txns : bool, optional
            set to True to include all the transactions data for each block
            (the default is False, which doesn't include transactions)

        Returns
        -------
        dict
            A python dictionary containing Blockchain data
        """

        data = {
            'current_block': self.current_block.block_hash,
            'genesis_block': self.genesis_block.block_hash,
            'total_blocks': len(self.blocks),
        }
        if blocks:
            data['blocks'] = [block.to_dict(txns) for block in self.blocks]
        return data
