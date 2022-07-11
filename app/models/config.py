from app import db

class config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    param = db.Column(db.String(50),unique=True)
    description = db.Column(db.String(500))
    value = db.Column(db.String(100))