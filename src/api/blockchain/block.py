from time import time
from hashlib import sha256
from merkletools import MerkleTools

from transaction import GenesisTransaction


class Block:

    NONCE_LEVEL = 3

    def __init__(self, index):
        # Block Header
        self.index = index
        self.timestamp = time()
        self.block_hash = None
        self.previous_hash = None
        self.nonce = 0

        self.next_block = None
        self.merkle_tree = MerkleTools()

        # Transaction
        self.transactions = []

    def __repr__(self):
        return 'Block({}, {}, {})'.format(
            self.index, self.timestamp, self.block_hash
        )

    def __str__(self):
        return 'Block // index:{} / timestamp:{} / block_hash:{}'.format(
            self.index, self.timestamp, self.block_hash
        )

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    # set the block hash and commit to chain
    def set_block_hash(self, parent):
        if parent is not None:
            self.previous_hash = parent.block_hash
            parent.next_block = self
        else:
            self.previous_hash = None

        self._build_merkle_tree()
        self.block_hash = self._calc_proof_of_work(
            self._calc_block_hash(self.previous_hash))

    def _build_merkle_tree(self):
        self.merkle_tree.reset_tree()
        for txn in self.transactions:
            self.merkle_tree.add_leaf(txn.calc_transaction_hash())

        self.merkle_tree.make_tree()

    def _calc_proof_of_work(self, block_hash):
        while True:
            guess = f'{block_hash}{self.nonce}'
            guess_hash = sha256(guess.encode('utf-8')).hexdigest()
            if guess_hash[:Block.NONCE_LEVEL] == '0' * Block.NONCE_LEVEL:
                return guess_hash
            else:
                self.nonce += 1

    # claclulate block hash based on previous hash
    def _calc_block_hash(self, previous_hash):
        blockheader = ''.join([
            str(self.index),
            str(self.timestamp),
            str(previous_hash)])

        block_data = ''.join([
            blockheader,
            str(self.merkle_tree.get_merkle_root())])

        return sha256(block_data.encode('utf-8')).hexdigest()

    # Check if chain is vlaid
    def is_valid_chain(self, previous_hash, verbose=True):
        is_valid = True
        self._build_merkle_tree()

        test_block = f'{self._calc_block_hash(previous_hash)}{self.nonce}'
        test_block_hash = sha256(test_block.encode('utf-8')).hexdigest()
        if test_block_hash != self.block_hash:
            is_valid = False
        else:
            is_valid = self.previous_hash == previous_hash

        self._print_verification_msg(is_valid, verbose)

        if self.next_block is not None:
            return self.next_block.is_valid_chain(test_block_hash, verbose)

        return is_valid

    # Chain verification helper
    def _print_verification_msg(self, is_valid, verbose):
        if verbose:
            if not is_valid:
                print('Block #{}: FAILED VERIFICATION!'.format(self.index))
            else:
                print('Block #{}: PASSED VERIFICATION'.format(self.index))

    def to_dict(self, txns=False):
        data = {
            'index': self.index,
            'timestamp': self.timestamp,
            'prev_hash': self.previous_hash,
            'block_hash': self.block_hash,
            'nonce': self.nonce,
            'merkle_root': self.merkle_tree.get_merkle_root()
        }
        if txns:
            data['tnxs'] = [txn.to_dict() for txn in self.transactions]
        return data


class GenesisBlock(Block):

    INDEX = 0

    def __init__(self):
        super().__init__(GenesisBlock.INDEX)
        self.add_transaction(GenesisTransaction())
        self.set_block_hash(None)
