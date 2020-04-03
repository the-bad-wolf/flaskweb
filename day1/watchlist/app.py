import os,sys

from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import click

WIN = sys.platform.startswith('win')
if WIN:
    prefix = "sqlite:///"
else:
    prefix = "sqlite:////"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,"data.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(10))

class movie(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.route("/")
def haha():
    movies = [
        {'title':"囧吗",'year':"2020"},
        {'title':"大赢家",'year':"2019"},
        {'title':"速度与激情",'year':"2018"},
        {'title':"叶问",'year':"2017"},
    ]
    return render_template('index.html',movies=movies)


@app.cli.command()
@click.option("--drop",is_flag=True,help="先删除在创建")
def initdb():
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("初始化数据库完成")



