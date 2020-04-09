
from watchlist import db,app
from models import *



import click

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
