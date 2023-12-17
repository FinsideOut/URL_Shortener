from datetime import datetime
from URL_Shortener import app, db, login_manager
from flask_login import UserMixin


class URL(db.Model):
    URL_id = db.Column(db.Integer, primary_key = True)
    long_URL = db.Column(db.String(300), nullable = False)
    allias = db.Column(db.String(20), unique = True, nullable = False)
    short_URL = db.Column(db.String(20), unique = True, nullable = False)
    date_added = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable = True)

    def __repr__(self):
        return f"{self.URL_id}, {self.long_URL}, {self.allias}, {self.short_URL}, {self.date_added}, {self.user_id}"
    

#handles user login verification for you??
@login_manager.user_loader
def loadUser(userId):
    return User.query.get(int(userId))

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)
    urls = db.relationship("URL", backref = "owner", lazy = True)
    

