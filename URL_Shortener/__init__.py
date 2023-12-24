import logging
import os
# from utils import build_logger
from openai import OpenAI
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

logging.basicConfig(level=logging.INFO,
                    filename = "log.log", 
                    filemode = "w", 
                    format = "%(asctime)s - %(levelname)s - %(message)s ")


# logger = build_logger()
# logger.info("APP RESTART \n")


app = Flask(__name__)
app.config["SECRET_KEY"] = "36a9c6555aab50f80218b5b516257036"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "temp_url.db")
app.config["RECAPTCHA_PUBLIC_KEY"] = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI" # Recaptcha test keys
app.config["RECAPTCHA_PRIVATE_KEY"] = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"

gpt_client = OpenAI()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
# login_manager.login_view = "main.home" # redirects to home if attempt to access restricted pages
# login_manager.login_message_category = "info" # info = bootstrap class

from URL_Shortener.users.routes import users
from URL_Shortener.main.routes import main
app.register_blueprint(users)
app.register_blueprint(main)



