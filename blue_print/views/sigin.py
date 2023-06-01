from flask import (
    Blueprint, render_template, request, redirect, url_for, session
)

bp = Blueprint('sigin', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    nm = request.form.get('username')
    pwd = request.form.get('password')
    session['username'] = nm
    if nm == 'luowenx' and pwd == 'qqq111':
        return redirect(url_for('index'))
    error = '用户名或密码错误，请重新登陆'
    return render_template('login.html', error=error)

@bp.route('/logout')
def logout():
    return 'logout'