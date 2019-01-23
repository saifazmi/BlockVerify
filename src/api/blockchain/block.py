from time import time
from hashlib import sha256
from merkletools import MerkleTools

from transaction import GenesisTransaction


class Block:
    """
    A class used to represent a Block in the Blockchain

    Attributes
    -------
    NONCE_LEVEL : int
        the difficulty level of the proof of work algorithm
    index : int
        the index number of the block
    timestamp : float
        the unix timestamp of the creation of this block
    block_hash : str
        the calculated proof of work hash of the block
    previous_hash : str
        the hash of the previous block
    nonce : int
        the nonce value for calculating the proof of work hash
    next_block : Block
        reference to the next block in the blockchain
    transactions : list
        list of transactions/records which are part of this block
    _merkle_tree : MerkleTools
        the merkle tree for all the transactions stored in this block

    Methods
    -------
    add_transaction(transaction)
        Adds a transaction to the block
    set_block_hash(parent)
        Sets the proof of work hash for this block
    _build_merkle_tree()
        Builds the Merkle Tree for the transactions of this block
    _clac_proof_of_work()
        Calculates and returns the proof of work hash for this block
    _calc_block_hash(previous_hash)
        Calculates the block hash
    is_valid_chain(previous_hash, verbose=True)
        Checks if the blockchain is valid
    to_dict(txns=False)
        Returns the block data as a python dictionary
    """

    NONCE_LEVEL = 3

    def __init__(self, index):
        """
        Parameters
        ----------
        index : int
            The index number of the block
        """

        # Block Header
        self.index = index
        self.timestamp = time()
        self.block_hash = None
        self.previous_hash = None
        self.nonce = 0

        self.next_block = None

        # Transactions
        self.transactions = []
        self._merkle_tree = MerkleTools()

    def __repr__(self):
        return 'Block({}, {}, {})'.format(
            self.index, self.timestamp, self.block_hash)

    def __str__(self):
        return 'Block // index:{} / timestamp:{} / block_hash:{}'.format(
            self.index, self.timestamp, self.block_hash)

    def __len__(self):
        return len(self.transactions)

    def add_transaction(self, transaction):
        """Adds a transaction to the list of transactions.

        Parameters
        ----------
        transaction : Transaction
            The transaction to add to the block
        """

        self.transactions.append(transaction)

    def set_block_hash(self, parent):
        """Sets the proof of work hash for this block.

        Builds the merkle tree of the transactions and calculates
        the proof of work hash value which is set as the block hash.

        Parameters
        ----------
        parent : Block
            Reference to the block preceding this block
        """

        if parent is not None:
            self.previous_hash = parent.block_hash
            parent.next_block = self
        else:
            self.previous_hash = None

        self._build_merkle_tree()
        self.block_hash = self._calc_proof_of_work()

    def _build_merkle_tree(self):
        """Builds the Merkle Tree for the transactions of this block."""

        self._merkle_tree.reset_tree()
        for txn in self.transactions:
            self._merkle_tree.add_leaf(txn.calc_transaction_hash())

        self._merkle_tree.make_tree()

    def _calc_proof_of_work(self):
        """Calculates and returns the proof of work hash for this block.

        Returns
        -------
        str
            The proof of work hash value of this block
        """

        while True:
            guess = f'{self._calc_block_hash(self.previous_hash)}{self.nonce}'
            guess_hash = sha256(guess.encode('utf-8')).hexdigest()
            if guess_hash[:Block.NONCE_LEVEL] == '0' * Block.NONCE_LEVEL:
                return guess_hash
            else:
                self.nonce += 1

    def _calc_block_hash(self, previous_hash):
        """Calculates the block hash.

        Calculates and sets the block hash based on the previous hash
        provided.

        Parameters
        ----------
        previous_hash : str
            Block hash of the preceding/parent block

        Returns
        -------
        str
            The calculated block hash value
        """

        blockheader = ''.join([
            str(self.index),
            str(self.timestamp),
            str(previous_hash),
            str(self.nonce)])

        block_data = ''.join([
            blockheader,
            str(self._merkle_tree.get_merkle_root())])

        return sha256(block_data.encode('utf-8')).hexdigest()

    def is_valid_chain(self, previous_hash=None, verbose=True):
        """Checks if the blockchain is valid.

        Recursively checks each block in the blockchain to verify if the
        whole blockchain is valid or not.

        Parameters
        ----------
        previous_hash : str, optional
            Block hash of the block preceding this one from which the validation
            process will start (the default is None, which validates the whole
            chain from the genesis block)
        verbose : bool, optional
            True to print  the validation status of each block in the
            blockchain, else False (the default is True)

        Returns
        -------
        bool
            True if the blockchain is valid else False
        """

        is_valid = True
        self._build_merkle_tree()

        test_block = f'{self._calc_block_hash(previous_hash)}{self.nonce}'
        test_block_hash = sha256(test_block.encode('utf-8')).hexdigest()
        if test_block_hash != self.block_hash and \
                test_block_hash[:Block.NONCE_LEVEL] != '0' * Block.NONCE_LEVEL:
            is_valid = False
        else:
            is_valid = self.previous_hash == previous_hash

        self._print_verification_msg(is_valid, verbose)

        if self.next_block is not None:
            return self.next_block.is_valid_chain(test_block_hash, verbose)

        return is_valid

    # Chain verification helper for verbose mode
    def _print_verification_msg(self, is_valid, verbose):
        if verbose:
            if not is_valid:
                print('Block #{}: FAILED VERIFICATION!'.format(self.index))
            else:
                print('Block #{}: PASSED VERIFICATION'.format(self.index))

    def to_dict(self, txns=False):
        """[summary]

        Parameters
        ----------
        txns : bool, optional
            [description] (the default is False, which [default_description])

        Returns
        -------
        [type]
            [description]
        """

        data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'prev_hash': self.previous_hash,
            'block_hash': self.block_hash,
            'nonce': self.nonce,
            'merkle_root': self._merkle_tree.get_merkle_root()
        }
        if txns:
            data['txns'] = [txn.to_dict() for txn in self.transactions]
        return data


class GenesisBlock(Block):

    INDEX = 0

    def __init__(self):
        super().__init__(GenesisBlock.INDEX)
        self.add_transaction(GenesisTransaction())
        self.set_block_hash(None)
