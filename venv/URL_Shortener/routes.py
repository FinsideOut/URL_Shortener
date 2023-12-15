from flask import render_template, redirect, url_for, flash
from URL_Shortener import app, db, gpt_client
from URL_Shortener.forms import URL_Form
from URL_Shortener.models import URL
from random import choice

def ask_gpt(topic):
    """Sumary: Calls open ai chat gpt 3.5 turbo and asks for a famous guote about topic
    Args:
        topic (string): the subject of the quote
    Returns:
        _type_: string tuple, quote and author
    """
    people = ["Steve Jobs", "Bill Gates", "Elon Musk"]
    person = choice(people)
    prompt = f"Find an inspirational quote by someone famous about{topic}. Don't give me any quotes longer than two sentences. If you don't understand {topic}, DON'T APOLOGIZE, just give me one at random from {person}."
    completion = gpt_client.chat.completions.create(model="gpt-3.5-turbo",messages=[
        {"role": "system", "content": prompt}
    ])
    return completion.choices[0].message.content.split("-")

def shorten_url(allias):
    return f"127.0.0.1:5000/{allias}"

@app.route("/",methods = ["GET", "POST"])
def home():
    form = URL_Form()
    place_holder = URL.query.get_or_404(1)
    if form.validate_on_submit():
        short_url = shorten_url(form.allias.data)
        new_URL = URL(long_URL = form.long_URL.data, allias = form.allias.data, short_URL = short_url)
        db.session.add(new_URL)
        db.session.commit()
        #quote,author = ask_gpt(form.allias.data)
        quote = "Test quote"
        author = "Me"
        flash(f"{quote} - {author}", "success")
        return render_template("index.html", title = "Home", form = form, short_url = short_url)
    return render_template("index.html", title = "Home", form = form)

@app.route("/<string:allias>")
def temp_url(allias):
    
    url = URL.query.filter_by(allias = allias).first()
    #print(url)
    return redirect(url.long_URL)
