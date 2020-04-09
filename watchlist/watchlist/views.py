from watchlist import app,db

from flask import Flask,render_template,request,flash,redirect,url_for
from flask_login import LoginManager,UserMixin,login_user,logout_user,login_required,current_user
from watchlist.models import *

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
        if username == user.username and user.validate_password(password):
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
