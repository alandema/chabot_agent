from flask import Flask, render_template, request
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv('config.env')
app = Flask(__name__)

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.2,
    max_tokens=500,
    timeout=None,
    max_retries=2
)


def get_completion(prompt):
    response = model.invoke(prompt)
    return response.content


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = get_completion(userText)
    return response


if __name__ == "__main__":
    app.run()
