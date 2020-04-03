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


@app.route("/",endpoint="index")
def haha():
    
    use = user.query.all()
    heiha = movie.query.all()
    return render_template('index.html',movies=heiha,use=user)


@app.cli.command()
@click.option("--drop",is_flag=True,help="先删除在创建")
def initdb():
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("初始化数据库完成")


#定义指令  然后flask+函数名  运行
@app.cli.command()
def forge():
    movies = [
        {'title':"囧吗",'year':"2020"},
        {'title':"大赢家",'year':"2019"},
        {'title':"速度与激情",'year':"2018"},
        {'title':"叶问",'year':"2017"},
    ]
    for m in movies:
        hei = movie(title=m['title'],year=m['year'])
        db.session.add(hei)
    db.session.commit()
    click.echo("导入数据完成")



#自定义404报错页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")





