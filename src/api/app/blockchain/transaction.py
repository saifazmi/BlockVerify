from hashlib import sha256
from queue import Queue
import os


class Transaction:

    def __init__(self, file_hash, author_key, signature):
        self.file_hash = file_hash
        self.author_key = author_key
        self.signature = signature

    def __repr__(self):
        return 'Transaction({}, {}, {})'.format(
            self.file_hash, self.author_key, self.signature
        )

    def __str__(self):
        return 'Transaction //\nfile_hash:{}\nauthor_key:{}\nsignature:{}' \
            .format(self.file_hash, self.author_key, self.signature)

    def calc_transaction_hash(self):
        txn = ''.join([self.file_hash, self.author_key, self.signature])
        return sha256(txn.encode('utf-8')).hexdigest()


class GenesisTransaction(Transaction):


    with open('genesis_files/py_zen.txt') as file_to_hash:
        data = file_to_hash.read()
        FILE_HASH = sha256(data.encode('utf-8')).hexdigest()
    with open('genesis_files/my_pgp_key.asc') as pub_key:
        AUTHOR_KEY = pub_key.read()
    with open('genesis_files/sign.asc') as sign:
        SIGNATURE = sign.read()

    def __init__(self):
        super().__init__(
            GenesisTransaction.FILE_HASH,
            GenesisTransaction.AUTHOR_KEY,
            GenesisTransaction.SIGNATURE
        )


class TransactionPool:

    def __init__(self):
        self._queue = Queue(maxsize=0)

    def __repr__(self):
        return 'TransactionPool(maxsize={})'.format(self._queue.maxsize)

    def __str__(self):
        return 'TransactionPool(maxsize={})\n{}'.format(
            self._queue.maxsize, self._queue.queue)

    def add_transaction(self, transaction):
        self._queue.put(transaction)

    def get_transaction(self):
        return self._queue.get()