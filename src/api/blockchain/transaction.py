from hashlib import sha256
from queue import Queue
import os


class Transaction:
    """
    A class used to represent a Transaction in the Block of a Blockchain.

    Attributes
    ----------
    file_hash : str
        SHA-256 hash of the file to be stored in the block
    author_key : str
        The openPGP public key of the file author used for signing the
        file hash
    signature : str
        The signature generated from signing the file hash with the
        author's key

    Methods
    -------
    calc_transaction_hash()
        Calculates the SHA-256 hash of this transaction
    to_dict()
        Returns the transaction data as a python dictionary
    from_dict()
        Creates a transaction object from the given python dictionary
    """

    def __init__(self, file_hash=None, author_key=None, signature=None):
        """
        Parameters
        -----------
        file_hash : str
            SHA-256 hash of the file to be stored in the block
        author_key : str
            The openPGP public key of the file author used for signing the
            file hash
        signature : str
            The signature generated from signing the file hash with the
            author's key
        """

        self.file_hash = file_hash
        self.author_key = author_key
        self.signature = signature

    def __repr__(self):
        return 'Transaction({}, {}, {})'.format(
            self.file_hash, self.author_key, self.signature)

    def __str__(self):
        return 'Transaction //\nfile_hash:{}\nauthor_key:{}\nsignature:{}' \
            .format(self.file_hash, self.author_key, self.signature)

    def calc_transaction_hash(self):
        """Calculates the SHA-256 hash of this transaction"""

        txn = ''.join([
            str(self.file_hash),
            str(self.author_key),
            str(self.signature)])
        return sha256(txn.encode('utf-8')).hexdigest()

    def to_dict(self):
        """Returns the transaction data as a python dictionary"""

        data = {
            'file_hash': self.file_hash,
            'author_key': self.author_key,
            'signature': self.signature
        }
        return data

    def from_dict(self, data):
        """Creates a transaction object from the given python dictionary

        Parameters
        ----------
        data : dict
            Data to generate a transaction object
        """
        for field in ['file_hash', 'author_key', 'signature']:
            if field in data:
                setattr(self, field, data[field])


class GenesisTransaction(Transaction):
    """A class used to represent a Genesis Transaction in the Blockchain."""

    basedir = os.path.abspath(os.path.dirname(__file__))
    genesis_dir = os.path.join(basedir, 'genesis_files')
    zen_file_path = os.path.join(genesis_dir, 'py_zen.txt')
    author_key_path = os.path.join(genesis_dir, 'my_pgp_key.asc')
    sign_path = os.path.join(genesis_dir, 'sign.asc')

    with open(zen_file_path) as file_to_hash:
        data = file_to_hash.read()
        FILE_HASH = sha256(data.encode('utf-8')).hexdigest()
    with open(author_key_path) as pub_key:
        AUTHOR_KEY = pub_key.read()
    with open(sign_path) as sign:
        SIGNATURE = sign.read()

    def __init__(self):
        super().__init__(
            GenesisTransaction.FILE_HASH,
            GenesisTransaction.AUTHOR_KEY,
            GenesisTransaction.SIGNATURE)


# not used
class TransactionPool:

    def __init__(self):
        self._queue = Queue(maxsize=0)

    def __repr__(self):
        return 'TransactionPool(maxsize={})'.format(self._queue.maxsize)

    def __str__(self):
        return 'TransactionPool(maxsize={})\n{}'.format(
            self._queue.maxsize, self._queue.queue)

    def add_transaction(self, transaction):
        self._queue.put(transaction, block=False)

    def get_transaction(self):
        return self._queue.get(block=False)

    def is_empty(self):
        return self._queue.empty()
