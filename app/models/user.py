from app import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    group = db.Column(db.String(35))
    enabled = db.Column(db.Boolean)
    resetpwd = db.Column(db.Boolean)