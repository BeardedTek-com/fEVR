from app import db

class cameras(db.Model):
# Table     : cameras
# Columns   : - id      (auto incrementing primary key)
#           : - camera  (Camera Name)
#           : - hls     (HLS stream URL)
#           : - rtsp    (RTSP stream URL)
    id = db.Column(db.Integer,primary_key = True)
    camera = db.Column(db.String(20), unique = True)
    hls = db.Column(db.String(200))
    rtsp = db.Column(db.String(200))
    show = db.Column(db.Boolean)