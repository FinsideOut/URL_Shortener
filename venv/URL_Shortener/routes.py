from flask import render_template, redirect, url_for, flash
from URL_Shortener import app, db
from URL_Shortener.forms import URL_Form
from URL_Shortener.models import URL

def shorten_url(allias):
    return f"https:/MyDomain/{allias}.com"

@app.route("/", methods = ["GET", "POST"])
@app.route("/home")
def home():
    form = URL_Form()
    short_url = "Your new URL goes Here!"
    if form.validate_on_submit():
        new_URL = URL(long_URL = form.long_URL.data, allias = form.allias.data, short_URL = shorten_url(form.allias.data))
        db.session.add(new_URL)
        db.session.commit()
        flash(f"Submitted {form.long_URL.data}", "success")
        return redirect(url_for("home"))

    return render_template("index.html", title = "Home", form = form, short_url = short_url)