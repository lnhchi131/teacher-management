from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from ..controllers.degrees_controller import get_degrees_data, add_degree_data, update_degree_data, delete_degree_data

bp = Blueprint('degree_routes', __name__)

@bp.route('/degrees')
@login_required
def degrees():
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    degrees = get_degrees_data()
    return render_template('degrees.html', degrees=degrees)

@bp.route('/degrees/add', methods=['GET', 'POST'])
@login_required
def degrees_add():
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    if request.method == 'POST':
        if add_degree_data(request.form):
            flash('Thêm bằng cấp thành công!')
            return redirect('/degrees')
        # Nếu lỗi, giữ lại form và hiển thị thông báo lỗi
        return render_template('degrees_form.html', degree=request.form)
    return render_template('degrees_form.html')

@bp.route('/degrees/edit/<int:degree_id>', methods=['GET', 'POST'])
@login_required
def degrees_edit(degree_id):
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    if request.method == 'POST':
        update_degree_data(request.form)
        flash('Cập nhật bằng cấp thành công!')
        return redirect('/degrees')
    degrees = get_degrees_data()
    degree = next((d for d in degrees if d[0] == degree_id), None)
    return render_template('degrees_form.html', degree=degree)

@bp.route('/degrees/delete/<int:degree_id>')
@login_required
def degrees_delete(degree_id):
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    if delete_degree_data(degree_id):
        flash('Xóa bằng cấp thành công!')
    else:
        flash('Không thể xóa vì bằng cấp đang được sử dụng!')
    return redirect('/degrees')