from flask import Flask, render_template, request, current_app
from ..chatbot.bot import get_completion

@current_app.route("/")
def home():
    return render_template("index.html")


@current_app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = get_completion(userText)
    return response