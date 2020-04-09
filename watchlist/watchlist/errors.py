
from watchlist import app
from flask import render_template

#自定义404报错页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")