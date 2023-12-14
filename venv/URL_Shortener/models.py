from datetime import datetime
from URL_Shortener import app, db

class URL(db.Model):
    URL_id = db.Column(db.Integer, primary_key = True)
    long_URL = db.Column(db.String(300), unique = True, nullable = False)
    allias = db.Column(db.String(20), unique = True, nullable = False)
    short_URL = db.Column(db.String(20), unique = True, nullable = False)