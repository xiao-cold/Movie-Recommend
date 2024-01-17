import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from database import db
from mydb import Users

# from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    print("register out")
    if request.method == 'POST':
        print("register in")
        username = request.form[
            'username']  # request.form is a special type of dict mapping submitted form keys and values. The user will input their username and password.
        password = request.form['password']
        # db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                # 生成整形的userId，自增
                userId = Users.query.count() + 2000
                user = Users(userId=userId, username=username, password=password)
                db.session.add(user)
                db.session.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))  # url_for(视图函数名)

        print("register error", error)
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    print("1111111111")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # db = get_db()
        error = None
        # 从数据库中查询用户
        print("22222222")
        user = Users.query.filter_by(username=username).first()
        print("查询用户" + "用户id", user.userId, "用户密码", user.password, "用户名称", user.username)

        if user is None:
            error = 'Incorrect username.'
        elif check_password_hash(user.password, password):
            error = 'Incorrect password.'
        if user.userId < 2000:
            g.user = user
            return redirect(url_for('recommend.manage'))
        if error is None:
            session.clear()
            session['user_id'] = user.userId
            g.user = user
            return redirect(url_for('recommend.index'))

        print(error)
        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    # session.clear() 会将session中的user_id删除
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        try:
            if g.user is None:
                return redirect(url_for('auth.login'))
        except(AttributeError):
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

#
# @bp.before_app_request
# def load_logged_in_user():
#     user_id = session.get('user_id')
#
#     if user_id is None:
#         g.user = Users.query.get(2008)
#     else:
#         g.user = Users.query.get(user_id)
