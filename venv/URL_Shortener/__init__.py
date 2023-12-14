import os
from flask import Flask
from URL_Shortener import forms
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "36a9c6555aab50f80218b5b516257036"

#chatGPT is the fucking BOMB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "test.db")

db = SQLAlchemy(app)

#test keys
app.config["RECAPTCHA_PUBLIC_KEY"] = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
app.config["RECAPTCHA_PRIVATE_KEY"] = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"

from URL_Shortener import routes

