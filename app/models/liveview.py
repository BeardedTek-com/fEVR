from app import db
    
class liveview(db.Model):
# Table     : liveview
#           Defines Live Camera View Layouts
# Columns   : - id      (auto incrementing primary key)
#           : - name    Name of layout
#           : - layout  Layout style (2x2, 4x4, etc)
#           : - members Comma separated list of camera id (from cameras table)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    layout = db.Column(db.String(10))
    members = db.Column(db.String(200))