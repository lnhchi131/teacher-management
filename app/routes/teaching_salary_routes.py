from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from ..controllers.teaching_salary_controller import calculate_teaching_salary
from ..models.teachers_model import get_teachers, get_teacher_by_code
from ..models.classes_model import get_semesters
import logging

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bp = Blueprint('teaching_salary_routes', __name__)

@bp.route('/teaching_salary', methods=['GET', 'POST'])
@login_required
def teaching_salary():
    # Lấy thông tin giáo viên hiện tại
    teacher = get_teacher_by_code(current_user.username) if current_user.role == 'teacher' else None
    teachers = get_teachers() if current_user.role in ['admin', 'department_admin'] else []
    semesters = get_semesters()
    salary_data = []
    total_salary = 0
    teacher_name = None
    selected_teacher = None
    selected_semester = None

    if request.method == 'POST':
        if current_user.role == 'teacher':
            selected_teacher = teacher[0] if teacher else None
            selected_semester = int(request.form['semester_id'])
            logger.debug(f"Teacher role: Calculating salary for teacher_id={selected_teacher}, semester_id={selected_semester}")
            if selected_teacher:
                salary_data, total_salary, teacher_name = calculate_teaching_salary(selected_teacher, semester_id=selected_semester)
        else:  # admin hoặc department_admin
            selected_teacher = int(request.form['teacher_id'])
            selected_semester = int(request.form['semester_id'])
            logger.debug(f"Admin/Dept role: Calculating salary for teacher_id={selected_teacher}, semester_id={selected_semester}")
            salary_data, total_salary, teacher_name = calculate_teaching_salary(selected_teacher, semester_id=selected_semester)
        logger.debug(f"Salary data: {salary_data}, Total: {total_salary}, Name: {teacher_name}")
        if not salary_data:
            flash('Không có dữ liệu lớp học cho giáo viên này trong kỳ học đã chọn.')

    return render_template('teaching_salary.html',
                           teachers=teachers,
                           semesters=semesters,
                           salary_data=salary_data,
                           total_salary=total_salary,
                           teacher_name=teacher_name,
                           selected_teacher=selected_teacher,
                           selected_semester=selected_semester)