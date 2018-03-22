import os
import hashlib
from app import app, gpg


def file_hash(filename):
    file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(file, 'rb') as fileToHash:
        data = fileToHash.read()
        sha256FileHash = hashlib.sha256(data).hexdigest()

    os.remove(file)
    return sha256FileHash


def file_signature(hash, keyid):
    return str(gpg.sign(hash, default_key=keyid))


def signature_key(keyid):
    return gpg.export_keys(keyid)
