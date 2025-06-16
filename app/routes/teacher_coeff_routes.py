from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from ..models.degrees_model import get_degrees, update_degree

bp = Blueprint('teacher_coeff_routes', __name__)

@bp.route('/degree_coeff', methods=['GET'])
@login_required
def degree_coeff_list():
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    degrees = get_degrees()
    return render_template('degree_coeff.html', degrees=degrees)

@bp.route('/degree_coeff/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def degree_coeff_edit(id):
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    degrees = get_degrees()
    degree = next((d for d in degrees if d[0] == id), None)
    if request.method == 'POST':
        update_degree(id, degree[1], float(request.form['coefficient']))
        flash('Cập nhật hệ số thành công!')
        return redirect('/degree_coeff')
    return render_template('degree_coeff_form.html', degree=degree)