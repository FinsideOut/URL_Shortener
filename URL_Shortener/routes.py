from flask import render_template, redirect, flash, request, jsonify
from URL_Shortener import app, db, bcrypt
from URL_Shortener.models import URL, User
from URL_Shortener.forms import URL_Form, Login_Form, Register_Form
from URL_Shortener.utils import ask_gpt, shorten_url



@app.route("/",methods = ["GET", "POST"])
def home():
    register_form = Register_Form()
    login_form = Login_Form()
    url_form = URL_Form()

    if url_form.validate_on_submit():
        # if url_form.check_allias():

        #quote = "Test quote"
        #author = "Me"
        #flash(f"{quote} - {author}", "success")
        return render_template("index.html", title = "Home", url_form = url_form, login_form = login_form, register_form = register_form, short_url = short_url, quote = quote, author = author)
    # if login_form.validate_on_submit():
    #     return render_template("index.html", title = "Home", url_form = url_form, login_form = login_form, register_form = register_form, short_url = short_url, quote = quote, author = author)
        

    return render_template("index.html", title = "Home", url_form = url_form, login_form = login_form,register_form = register_form)

@app.route('/url_submit', methods=['POST'])
def url_submit():
    form = URL_Form(request.form)
    if form.validate_on_submit():
        short_url = shorten_url(form.allias.data)
        new_URL = URL(long_URL = form.long_URL.data, allias = form.allias.data, short_URL = short_url)
        db.session.add(new_URL)
        db.session.commit()
        quote,author = ask_gpt(form.allias.data)
        return jsonify(success=True,
                        quote = quote, 
                        author = author,
                        result = f"127.0.0.1:5000/{form.allias.data}")
    else:
        # Return a response with errors if validation fails
        errors = {field.name: field.errors for field in form}
        return jsonify(success=False, errors=errors)

@app.route('/register_submit', methods=['POST'])
def register_submit():
    form = Register_Form(request.form)
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username = form.username.data, 
                        email = form.email.data,
                        password = hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(success=True)
    else:
        # Return a response with errors if validation fails
        errors = {field.name: field.errors for field in form}
        return jsonify(success=False, errors=errors)

@app.route('/login_submit', methods=['POST'])
def login_submit():
    form = Login_Form(request.form)
    if form.validate_on_submit():
        return jsonify(success=True)
    else:
        # Return a response with errors if validation fails
        errors = {field.name: field.errors for field in form}
        return jsonify(success=False, errors=errors)

@app.route("/<string:allias>")
def temp_url(allias):
    if allias:
        url = URL.query.filter_by(allias = allias).first()
        if url:
            return redirect(url.long_URL)
    return render_template("404.html")

# @app.route("/submit-registration", methods = ["GET"])
# def submit_registration():
#     form = Register_Form()
#     if form.check_user_exists():
#         return jsonify({"value": True})
#     else:
#         return jsonify({"value": False})


# @app.route("/submit-login", methods = ["GET"])
# def submit_login():
#     login_form = Login_Form()
#     user = User.query.filter_by(email = login_form.email.data).first()
#     if user and bcrypt.check_password_hash(user.password, login_form.password.data):
#         return jsonify({"username": True,
#                         "password": True})
#     elif user:
#         return jsonify({"username": True,
#                         "password": False})
#     else:
#         return jsonify({"username": False,
#                         "password": False})
         


        

    