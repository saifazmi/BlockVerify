from app import db, login, gpg
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    key_fingerprint = db.Column(db.String(60), unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Password utils
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # GPG key
    def set_key(self, key_length=1024):
        self.key_fingerprint = self._gen_key(key_length).fingerprint

    def _gen_key(self, key_length):
        batch_key_input = gpg.gen_key_input(
            name_real=self.username,
            name_email=self.email,
            key_type='RSA',
            key_length=key_length,
        )
        return gpg.gen_key(batch_key_input)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
