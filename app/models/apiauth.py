from app import db
from flask_login import UserMixin

class apiAuth(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),unique=True)
    key = db.Column(db.String(150),unique=True)
    authIP = db.Column(db.String(20))
    limit = db.Column(db.Integer)
    expired = db.Column(db.Boolean)