from URL_Shortener.people import people
from URL_Shortener import gpt_client, app
from flask import jsonify
import logging
from random import choice

def ask_gpt(topic):
    # """Sumary: Calls open ai chat gpt 3.5 turbo and asks for a famous guote about topic
    # Args:
    #     topic (string): the subject of the quote
    # Returns:
    #     _type_: string tuple, quote and author
    # """
    # people = ["Steve Jobs", "Bill Gates", "Elon Musk"]
    # person = choice(people)
    # prompt = f"Find an inspirational quote by someone famous related to {topic}. Don't give me any quotes longer than two sentences. If you don't understand {topic}, or {topic} is just random letters or numbers, DON'T APOLOGIZE, just give me a quote from {person}. DO NOT make a quote up yourself and attribute it to 'unkown'"
    # completion = gpt_client.chat.completions.create(model="gpt-3.5-turbo",messages=[
    #     {"role": "system", "content": prompt}
    # ])
    # return completion.choices[0].message.content.split("-")
    return ("QUOTE","AUTHOR")

def get_examples():
    # prompt = f"give me a single random word. ONLY ONE WORD, NO OTHER RESPONSE"
    # completion = gpt_client.chat.completions.create(model="gpt-3.5-turbo",messages=[
    #     {"role": "system", "content": prompt}
    # ])
    # allias = completion.choices[0].message.content

    # prompt = f"give me a random url that is related to {allias}. The url should be difficult to read. ONLY RETURN THE URL. DO NOT CONFIRM YOUR ACTIONS WITH ANY WORDS"
    # completion = gpt_client.chat.completions.create(model="gpt-3.5-turbo",messages=[
    #     {"role": "system", "content": prompt}
    # ])
    # url = completion.choices[0].message.content
    url = "url"
    allias = "allias"
    return (url, allias)


def shorten_url(allias):
    return f"127.0.0.1:5000/{allias}"


def build_logger():
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler("debugging.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger