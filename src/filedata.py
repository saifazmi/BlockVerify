import hashlib


def _file_hash(file):
    with open(file, 'rb') as fileToHash:
        data = fileToHash.read()
        sha256FileHash = hashlib.sha256(data).hexdigest()

    return sha256FileHash
