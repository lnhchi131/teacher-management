from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from ..controllers.class_coefficients_controller import (
    get_class_coefficients_data, add_class_coefficient_data, update_class_coefficient_data, delete_class_coefficient_data
)

bp = Blueprint('class_coefficients_routes', __name__)

@bp.route('/class_coeff', methods=['GET'])
@login_required
def class_coeff_list():
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    data = get_class_coefficients_data()
    return render_template('class_coefficients.html', data=data)

@bp.route('/class_coeff/add', methods=['GET', 'POST'])
@login_required
def class_coeff_add():
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    if request.method == 'POST':
        add_class_coefficient_data(request.form)
        flash('Thêm hệ số lớp thành công!')
        return redirect('/class_coeff')
    return render_template('class_coefficients_form.html')

@bp.route('/class_coeff/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def class_coeff_edit(id):
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    data = get_class_coefficients_data()
    coeff = next((c for c in data if c[0] == id), None)
    if request.method == 'POST':
        if update_class_coefficient_data(request.form):
            flash('Cập nhật hệ số lớp thành công!')
            return redirect('/class_coeff')
        # Nếu lỗi, giữ lại form và hiển thị thông báo lỗi
        return render_template('class_coefficients_form.html', coeff=request.form)
    return render_template('class_coefficients_form.html', coeff=coeff)

@bp.route('/class_coeff/delete/<int:id>')
@login_required
def class_coeff_delete(id):
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    delete_class_coefficient_data(id)
    flash('Xóa hệ số lớp thành công!')
    return redirect('/class_coeff')