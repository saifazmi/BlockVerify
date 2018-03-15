from time import time


class Block:

    def __init__(self, index, nounce, previous_hash, transactions=None):
        self.index = index
        self.time_stamp = time()  # unix time
        self.nounce = nounce
        self.previous_hash = previous_hash

        if transactions is None:
            self.transactions = []
        else:
            self.transactions = transactions


if __name__ == "__main__":
    pass
