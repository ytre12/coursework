from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Forest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mainForest = db.Column(db.String(100), nullable=False)
    forest = db.Column(db.String(100), nullable=False)
    typeCutting = db.Column(db.String(100), nullable=False)
    quarter = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    area = db.Column(db.Float, nullable=False)
    volumeForestManagement = db.Column(db.Float, nullable=False)    
    month = db.Column(db.String(50), nullable=False)
    decade = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)

class Comits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isAdmin = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    gmail = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Forum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(150), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    forestID = db.Column(db.Integer, db.ForeignKey('forest.id'), nullable=False)