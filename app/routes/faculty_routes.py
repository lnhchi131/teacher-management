from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from ..controllers.faculties_controller import get_faculties_data, add_faculty_data, update_faculty_data, delete_faculty_data

bp = Blueprint('faculty_routes', __name__)

@bp.route('/faculties')
@login_required
def faculties():
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    faculties = get_faculties_data()
    return render_template('faculties.html', faculties=faculties)

@bp.route('/faculties/add', methods=['GET', 'POST'])
@login_required
def faculties_add():
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    if request.method == 'POST':
        if add_faculty_data(request.form):
            flash('Thêm khoa thành công!')
            return redirect('/faculties')
        # Nếu lỗi, giữ lại form và hiển thị thông báo lỗi
        return render_template('faculties_form.html', faculty=request.form)
    return render_template('faculties_form.html')

@bp.route('/faculties/edit/<int:faculty_id>', methods=['GET', 'POST'])
@login_required
def faculties_edit(faculty_id):
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    if request.method == 'POST':
        if update_faculty_data(request.form):
            flash('Cập nhật khoa thành công!')
            return redirect('/faculties')
    faculties = get_faculties_data()
    faculty = next((f for f in faculties if f[0] == faculty_id), None)
    return render_template('faculties_form.html', faculty=faculty)

@bp.route('/faculties/delete/<int:faculty_id>')
@login_required
def faculties_delete(faculty_id):
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    if delete_faculty_data(faculty_id):
        flash('Xóa khoa thành công!')
    else:
        flash('Không thể xóa vì khoa đang có giáo viên!')
    return redirect('/faculties')