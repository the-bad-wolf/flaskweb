from flask import Flask


app = app = Flask(__name__)


app.route("/",endpoint="index")
def haha():
    return “<h1>hello world</h1> ”






