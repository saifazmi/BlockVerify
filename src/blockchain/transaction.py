from hashlib import sha256

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
