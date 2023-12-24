from flask import render_template, Blueprint
from URL_Shortener import app, db
from URL_Shortener.users.forms import Login_Form, Register_Form
from URL_Shortener.links.forms import URL_Form
from URL_Shortener.utils import ask_gpt, get_examples

from URL_Shortener.utils import build_logger

logger = build_logger()

main = Blueprint("main", __name__)


@main.route("/",methods = ["GET", "POST"])
def home():
    register_form = Register_Form()
    login_form = Login_Form()
    url_form = URL_Form()
    long_example, allias_example = get_examples()
    quote, author = ask_gpt(allias_example)
    return render_template("index.html", title = "Home", url_form = url_form, login_form = login_form, register_form = register_form, quote = quote, author = author, long_example = "Example: " + long_example, allias_example = "Example: " + allias_example)









        

    