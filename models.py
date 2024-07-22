# from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import Flask
from datetime import datetime

NULLABLE = {'nullable': True}

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    is_active = db.Column(db.Boolean(), default=True)

    def __str__(self):
        return self.login

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(255))
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    image = db.Column(db.String(255))

    def __str__(self):
        return self.title


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    post = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)

    def __str__(self):
        return f'{self.comment} - {self.timestamp}'


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50))
    user = db.Column(db.Integer, db.ForeignKey('user.id'), **NULLABLE)
    post = db.Column(db.Integer, db.ForeignKey('post.id'), **NULLABLE)
