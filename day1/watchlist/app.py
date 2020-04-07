import os,sys

from flask import Flask,render_template,request,flash,redirect,url_for
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
app.config["SECRET_KEY"] = "1903_dev"


db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(10))

class movie(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


@app.route("/",endpoint="index",methods=["post","get"])
def haha():
    if request.method.lower() == "post":
        title = request.form.get("title")
        year = request.form.get("year")
        if not title or not year or len(year)>4:
            flash("输入错误！")
            return redirect(url_for("index"))
        ha = movie(title=title,year=year)
        db.session.add(ha)
        db.session.commit()
        flash("创建成功")
        return redirect(url_for("index"))

    heiha = movie.query.all()
    return render_template('index.html',movies=heiha)

@app.route("/movie/edit/<int:movie_id>",methods=['get','post'],endpoint="edit")
def edit(movie_id):
    heiha = movie.query.get_or_404(movie_id)
    if request.method.lower() ==  "post":
        title = request.form.get("title")
        print(title)
        year = request.form.gte("year")
        if not title or not year or len(year)>4:
            flash("输入错误")
            print("22222222222222222222222222222222")
            return redirect(url_for("edit"), movie_id=movie_id)
        heiha.title = title
        heiha.year = year
        db.session.commit()
        flash("电影更新完成")
        return redirect(url_for("index"))
    return render_template("edit.html",movie=heiha)


@app.route("/delete/edit/<int:movie_id>",methods=['get','post'],endpoint="delete")
def delete(movie_id):
    heiha = movie.query.get_or_404(movie_id)
    db.session.delete(heiha)
    db.session.commit()
    flash("删除完成")
    return redirect(url_for("index"))



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




#模板上下文处理函数
@app.context_processor
def common_user():
    heiha = user.query.all()
    return dict(use=heiha)



