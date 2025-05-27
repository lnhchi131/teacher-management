from flask import Blueprint, render_template, request, redirect, session, flash
from flask_login import login_user, logout_user, login_required, current_user

bp = Blueprint('routes', __name__)

@bp.route('/')
@login_required
def index():
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        from ..models.users_model import get_user_by_username
        username = request.form['username']
        password = request.form['password']
        user, stored_password = get_user_by_username(username)
        if user and stored_password == password:
            login_user(user)
            return redirect('/')
        flash('Tên đăng nhập hoặc mật khẩu không đúng!')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')