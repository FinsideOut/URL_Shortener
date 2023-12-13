from flask import render_template
from URL_Shortener import app
print("YO!")
@app.route("/")
@app.route("/home")

def home():
    return render_template("index.html")