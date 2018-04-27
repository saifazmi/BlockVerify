import os
import sys

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    BLOCKCHAIN_PATH = os.environ.get('BLOCKCHAIN_PATH') or os.path.join(
        basedir, 'blockchain')
    sys.path.insert(0, BLOCKCHAIN_PATH)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
