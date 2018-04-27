import os
import hashlib
from app import app, gpg


def file_hash(filename):
    file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(file, 'rb') as file_to_hash:
        data = file_to_hash.read()
        sha256_file_hash = hashlib.sha256(data).hexdigest()

    os.remove(file)
    return sha256_file_hash


def file_signature(hash, keyid):
    return str(gpg.sign(hash, default_key=keyid))


def signature_key(keyid):
    return gpg.export_keys(keyid)
