from app import db


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_hash = db.Column(db.String(64), index=True, unique=True)
    block_hash = db.Column(db.String(64))
    block_index = db.Column(db.Integer)
    txn_index = db.Column(db.Integer)
