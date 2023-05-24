from passlib.hash import pbkdf2_sha256

from flask_poetry_api import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def encrypt_password(self) -> None:
        self.password = pbkdf2_sha256.hash(self.password)

    def check_password(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password)
