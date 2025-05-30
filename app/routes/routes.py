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
            # Lưu thông tin role và department_id vào session
            session['role'] = user.role
            session['department_id'] = user.department_id
            return redirect('/')
        flash('Tên đăng nhập hoặc mật khẩu không đúng!')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    session.pop('role', None)
    session.pop('department_id', None)
    logout_user()
    return redirect('/login')