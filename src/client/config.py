import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GPG_KEY_STORE = os.environ.get('GPG_KEY_STORE') or os.path.join(
        basedir, 'keys')
    GPG_BINARY = os.environ.get('GPG_BINARY') or '/usr/bin/gpg1'
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(
        basedir, 'uploads')
    ALLOWED_EXTENSIONS = []
