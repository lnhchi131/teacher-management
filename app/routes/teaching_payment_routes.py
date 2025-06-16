from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from ..controllers.teaching_rate_controller import get_rate_data, update_rate_data

bp = Blueprint('teaching_payment_routes', __name__)

@bp.route('/teaching_rate', methods=['GET', 'POST'])
@login_required
def teaching_rate():
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    if request.method == 'POST':
        update_rate_data(request.form)
        flash('Cập nhật định mức tiền tiết thành công!')
        return redirect('/teaching_rate')
    rate = get_rate_data()
    return render_template('teaching_rate.html', rate=rate)