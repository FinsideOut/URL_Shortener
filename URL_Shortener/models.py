from datetime import datetime
from URL_Shortener import app, db, login_manager
from flask_login import UserMixin


class URL(db.Model):
    URL_id = db.Column(db.Integer, primary_key = True)
    long_URL = db.Column(db.String(300), nullable = False)
    allias = db.Column(db.String(20), unique = True, nullable = False)
    short_URL = db.Column(db.String(20), unique = True, nullable = False)
    date_added = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_expired = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    life_span = db.Column(db.Integer, nullable = False, default = 3)
    active = db.Column(db.Boolean, nullable = False, default = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable = True)

    def __repr__(self):
        return f"ID:{self.URL_id}, LONG:{self.long_URL}, ALLIAS:{self.allias}, SHORT:{self.short_URL}, DATE:{self.date_added}, LIFESPAN:{self.life_span} ACTIVE:{self.active} USER_ID:{self.user_id}"
    

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

    # must be there to allow "login_user()" to work
    def get_id(self):
        return str(self.user_id)
    
    def __repr__(self):
        return f"USER(user_id={self.user_id}, USERNAME='{self.username}', EMAIL='{self.email}')"

