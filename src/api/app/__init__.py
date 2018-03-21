from flask import Flask
from config import Config

from blockchain import Blockchain

app = Flask(__name__)
app.config.from_object(Config)

chain = Blockchain()

from app import routes
