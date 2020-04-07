import os,sys

from flask import Flask,render_template,request,flash,redirect,url_for
from werkzeug.security import check_password_hash,generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required,current_user
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
login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    return user
login_manager.login_view = 'login'


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(10))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    def validate_password(self,password):
        return check_password_hash(self.password_hash,password)

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
@login_required
def edit(movie_id):
    heiha = movie.query.get_or_404(movie_id)
    if request.method.lower() ==  "post":
        title = request.form.get("title")
        print(title)
        year = request.form.gte("year")
        if not title or not year or len(year)>4:
            flash("输入错误")
            return redirect(url_for("edit"), movie_id=movie_id)
        heiha.title = title
        heiha.year = year
        db.session.commit()
        flash("电影更新完成")
        return redirect(url_for("index"))
    return render_template("edit.html",movie=heiha)


@app.route("/delete/edit/<int:movie_id>",methods=['get','post'],endpoint="delete")
@login_required
def delete(movie_id):
    heiha = movie.query.get_or_404(movie_id)
    db.session.delete(heiha)
    db.session.commit()
    flash("删除完成")
    return redirect(url_for("index"))

#登陆
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('输入有误')
            return redirect(url_for('login'))
        user = User.query.first()
        print(11111111111111111111111111111111111111111111111111111)
        if username == user.username and user.validate_password(password):
            print(22222222222222222222222222222222222222222222222222222222222222222222222222222222222222222)
            login_user(user)
            flash('登录成功')
            return redirect(url_for('index'))
        flash('验证失败')
        return redirect(url_for('login'))
    return render_template('login.html')


 #退出   
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出成功')
    return redirect(url_for('index'))


# settings 设置
@app.route('/settings',methods=['POST','GET'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name)>20:
            flash('输入错误')
            return redirect(url_for('settings'))
        current_user.name = name
        db.session.commit()
        flash('名字已经更新')
        return redirect(url_for('index'))
    return render_template('settings.html')




@app.cli.command()
@click.option('--drop',is_flag=True,help="先删除在创建")
def initdb(drop):
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
    user = User.query.all()
    return dict(use=user)

@app.cli.command()
@click.option('--username',prompt=True,help='登录的用户名')
@click.option('--password',prompt=True,help='登录的密码',confirmation_prompt=True,hide_input=True)
def admin(username,password):
    user = User.query.first()
    if ha is not None:
        click.echo('更新管理员用户')
        user.username = username
        ha.set_password(password)
    else:
        click.echo('创建管理员账户')
        user = User(username=username,name='Admin')
        user.set_password(password)
        db.session.add(ha)
    
    db.session.commit()
    click.echo('管理员账号更新/创建完成')
