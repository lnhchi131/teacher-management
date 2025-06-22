from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from ..controllers.teachers_controller import get_teachers_data, get_teacher_data, add_teacher_data, update_teacher_data, delete_teacher_data, get_teacher_form_data
from ..controllers.degrees_controller import get_degrees_data
from ..controllers.faculties_controller import get_faculties_data
from ..controllers.classes_controller import get_assigned_classes_data
from ..models.teachers_model import get_teacher_by_code
import logging

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bp = Blueprint('teacher_routes', __name__)

@bp.route('/teachers')
@login_required
def teachers():
    teachers = get_teachers_data()
    degrees = get_degrees_data()
    faculties = get_faculties_data()
    stats = [(degree[1], degree[3]) for degree in degrees] + [(faculty[2], faculty[4]) for faculty in faculties]
    return render_template('teachers.html', teachers=teachers, stats=stats)

@bp.route('/teachers/add', methods=['GET', 'POST'])
@login_required
def teachers_add():
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    if request.method == 'POST':
        if add_teacher_data(request.form):
            flash('Thêm giáo viên thành công!')
            return redirect('/teachers')
        # Nếu lỗi, giữ lại form và dữ liệu đã nhập
        form_data = get_teacher_form_data()
        return render_template('teachers_form.html',
                               departments=form_data['departments'],
                               degrees=form_data['degrees'],
                               teacher=request.form)  # truyền lại dữ liệu đã nhập
    form_data = get_teacher_form_data()
    return render_template('teachers_form.html', departments=form_data['departments'], degrees=form_data['degrees'])

@bp.route('/teachers/edit/<int:teacher_id>', methods=['GET', 'POST'])
@login_required
def teachers_edit(teacher_id):
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    if request.method == 'POST':
        if update_teacher_data(request.form):
            flash('Cập nhật giáo viên thành công!')
            return redirect('/teachers')
        # Nếu lỗi, giữ lại form và hiển thị thông báo lỗi
        teacher = get_teacher_data(teacher_id)
        form_data = get_teacher_form_data()
        return render_template('teachers_form.html', teacher=teacher, departments=form_data['departments'], degrees=form_data['degrees'])
    teacher = get_teacher_data(teacher_id)
    form_data = get_teacher_form_data()
    return render_template('teachers_form.html', teacher=teacher, departments=form_data['departments'], degrees=form_data['degrees'])

@bp.route('/teachers/delete/<int:teacher_id>')
@login_required
def teachers_delete(teacher_id):
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    delete_teacher_data(teacher_id)
    flash('Xóa giáo viên thành công!')
    return redirect('/teachers')

@bp.route('/profile')
@login_required
def teacher_profile():
    if current_user.role != 'teacher':
        flash('Chỉ giáo viên mới có quyền truy cập!')
        return redirect('/')
    # Lấy thông tin giáo viên dựa trên username (code trong teachers)
    teacher = get_teacher_by_code(current_user.username)
    if not teacher:
        flash('Không tìm thấy thông tin giáo viên!')
        return redirect('/')
    teacher_id = teacher[0] if teacher else None
    logger.debug(f"Teacher ID: {teacher_id}, Username: {current_user.username}")
    assigned_classes = get_assigned_classes_data(teacher_id) if teacher_id else []
    logger.debug(f"Assigned classes for teacher_id {teacher_id}: {assigned_classes}")
    return render_template('teacher_profile.html', teacher=teacher, assigned_classes=assigned_classes)

@bp.route('/stats')
@login_required
def stats():
    degrees = get_degrees_data()
    faculties = get_faculties_data()
    if current_user.role == 'department_admin':
        # Chỉ lấy faculty của mình
        faculties = [f for f in faculties if f[0] == current_user.department_id]
        # Chỉ thống kê giáo viên khoa mình cho từng bằng cấp
        from ..models.teachers_model import get_teachers_by_department
        teachers = get_teachers_by_department(current_user.department_id)
        # Đếm số giáo viên theo bằng cấp trong khoa mình
        degree_stats = []
        for degree in degrees:
            count = sum(1 for t in teachers if t[7] == degree[1])
            degree_stats.append((degree[1], count))
        # Thống kê theo khoa chỉ có khoa mình
        faculty_stats = [(faculties[0][2], len(teachers))]
        stats = degree_stats + faculty_stats
    else:
        # Admin: thống kê toàn bộ
        stats = [(degree[1], degree[3]) for degree in degrees] + [(faculty[2], faculty[4]) for faculty in faculties]
    return render_template('stats.html', stats=stats)