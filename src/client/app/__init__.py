from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from gnupg import GPG
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

gpg = GPG(
    binary='/usr/bin/gpg1',
    homedir=app.config['GPG_KEY_STORE'],
    keyring='pubring.gpg',
    secring='secring.gpg')

from app import routes, models
