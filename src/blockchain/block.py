from time import time
from hashlib import sha256


class Block:

    def __init__(self, index, parent, file_hash, author_key,
                 signature):
        # Block Header
        self.index = index
        self.timestamp = time()
        self.block_hash = None
        self.previous_hash = None
        self.next_block = None

        # Transactions
        self.file_hash = file_hash
        self.author_key = author_key
        self.signature = signature

        self._set_block_hash(parent)

    # def __repr__(self):
    #     pass

    # def __str__(self):
    #     pass

# set the block hash and commit to chain
    def _set_block_hash(self, parent):
        if parent is not None:
            self.previous_hash = parent.block_hash
            parent.next_block = self
        else:
            self.previous_hash = None

        self.block_hash = self._calc_block_hash(self.previous_hash)

    # claclulate block hash based on previous hash
    def _calc_block_hash(self, previous_hash):
        blockheader = ''.join([
            str(self.index),
            str(self.timestamp),
            str(previous_hash)])

        txn = ''.join([
            self.file_hash,
            self.author_key,
            self.signature])

        block = ''.join([blockheader, txn])
        return sha256(block.encode('utf-8')).hexdigest()

    # Check if valid chain
    def is_valid_chain(self, previous_hash, verbose=True):
        is_valid = False

        test_block_hash = self._calc_block_hash(previous_hash)
        if test_block_hash != self.block_hash:
            is_valid = False
        else:
            is_valid = self.previous_hash == previous_hash

        self._print_verification_msg(is_valid, verbose)

        if self.next_block is not None:
            return self.next_block.is_valid_chain(test_block_hash, verbose)

        return is_valid

    def _print_verification_msg(self, is_valid, verbose):
        if verbose:
            if not is_valid:
                print('Block #{}: FAILED VERIFICATION'.format(self.index))
            else:
                print('Block #{}: PASSED VERIFICATION'.format(self.index))
