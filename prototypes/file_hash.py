#!/usr/bin/env python

import sys
import hashlib


file = sys.argv[1]
# this line of code works,
# BUT re-write it using a "with" block to handle file properly.
file_hash = hashlib.sha256(open(file, 'rb').read()).hexdigest()

print(file_hash)


def file_hash(file):
    # open file
    with open(file, 'rb') as fileToHash:
        data = fileToHash.read()
        sha256FileHash = hashlib.sha256(data).hexdigest()

    return sha256FileHash


print(file_hash(file))
