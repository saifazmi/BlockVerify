#!/bin/python

import sys
import hashlib


file = sys.argv[1]
# this line of code words,
# BUT re-write it using a "with" block to handle file properly.
file_hash = hashlib.sha256(open(file, 'rb').read()).hexdigest()

print(file_hash)


def file_hash(file):
    # open file
    with open(file, 'rb') as file_to_hash:
        data = file_to_hash.read()
        file_sha256_hash = hashlib.sha256(data).hexdigest()

    return file_sha256_hash


print(file_hash(file))
