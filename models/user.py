from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Связь с результатами тестов
    results = db.relationship('QuizResult', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User {self.email}>"
