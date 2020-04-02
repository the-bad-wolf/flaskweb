from flask import Flask,render_template


app = Flask(__name__)


@app.route("/")
def haha():
    movies = [
        {'title':"囧吗",'year':"2020"},
        {'title':"大赢家",'year':"2019"},
        {'title':"速度与激情",'year':"2018"},
        {'title':"叶问",'year':"2017"},
    ]
    return render_template('index.html',movies=movies)






