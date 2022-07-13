from app import db

class frigate(db.Model):
# Table     : frigate
# Columns   : - id      (auto incrementing primary key)
#           : - url     (URL of frigate instance ex: http://192.168.101.10:5000)
#           : - name    (MQTT name of frigate instance)
    id = db.Column(db.Integer,primary_key = True)
    url = db.Column(db.String(200))
    name = db.Column(db.String(100), unique = True)