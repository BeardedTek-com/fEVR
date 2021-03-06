from app import db
from datetime import datetime

class events(db.Model):
# Table     : events
# Columns   : - id      (auto incrementing primary key)
#           : - eventid (Event ID from Frigate)
#           : - time    (DateTime generated from eventid timestamp)
#           : - camera  (Camera which generated event)
#           : - object  (Type of object detected)
#           : - score   (Score generated by frigate (math.floor(frigate_score*100)))
#           : - ack     (blank if unacknowledged, 'true' if acknowledged This is a string so that it can be set to "","ack","seen","delete")
    id = db.Column(db.Integer,primary_key = True)
    eventid = db.Column(db.String(25), unique = True)
    time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    camera = db.Column(db.String(50))
    object = db.Column(db.String(25))
    score = db.Column(db.Integer)
    ack = db.Column(db.String(10))
    show = db.Column(db.Boolean)