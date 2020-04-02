from flask import Flask


app = app = Flask(__name__)


@app.route("/")
def haha():
    return "<h1>hello world</h1>"






