from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from ..controllers.teaching_salary_controller import calculate_teaching_salary
from ..models.teachers_model import get_teachers
from ..models.classes_model import get_semesters

bp = Blueprint('teaching_salary_routes', __name__)

@bp.route('/teaching_salary', methods=['GET', 'POST'])
@login_required
def teaching_salary():
    teachers = get_teachers()
    semesters = get_semesters()
    salary_data = []
    total_salary = 0
    teacher_name = None
    selected_teacher = None
    selected_semester = None
    if request.method == 'POST':
        selected_teacher = int(request.form['teacher_id'])
        selected_semester = int(request.form['semester_id'])
        salary_data, total_salary, teacher_name = calculate_teaching_salary(selected_teacher, selected_semester)
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