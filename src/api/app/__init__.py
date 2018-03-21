from flask import Flask
from config import Config

from blockchain import Blockchain

app = Flask(__name__)
app.config.from_object(Config)

blockchain = Blockchain()

from app import routes
