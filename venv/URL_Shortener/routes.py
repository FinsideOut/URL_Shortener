from flask import render_template, redirect, url_for, flash
from URL_Shortener import app
from URL_Shortener.forms import URL_Form

@app.route("/", methods = ["GET", "POST"])
@app.route("/home")
def home():
    form = URL_Form()
    if form.validate_on_submit():
        flash(f"Submitted {form.long_url}", "success")
        return redirect(url_for("home"))
    else:
        print(form.errors)
        print("Validation Failed")
    return render_template("index.html", title = "Home", form = form)