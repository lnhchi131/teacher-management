from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from ..controllers.teaching_salary_controller import (
    report_teacher_salary_by_year,
    report_department_salary_by_year,
    report_school_salary_by_year
)
from ..models.teachers_model import get_teachers
from ..controllers.classes_controller import get_academic_years

bp = Blueprint('teaching_report_routes', __name__)

@bp.route('/report/teacher_salary', methods=['GET', 'POST'])
@login_required
def report_teacher_salary():
    teachers = get_teachers()
    academic_years = get_academic_years()
    report_data = []
    total_salary = 0
    teacher_name = None
    selected_teacher = None
    selected_year = None
    if request.method == 'POST':
        selected_teacher = int(request.form['teacher_id'])
        selected_year = request.form['academic_year']
        report_data, total_salary, teacher_name = report_teacher_salary_by_year(selected_teacher, selected_year)
        if not report_data:
            flash('Không có dữ liệu lớp học cho giáo viên này trong năm học đã chọn.')
    return render_template('report_teacher_salary.html',
                           teachers=teachers,
                           academic_years=academic_years,
                           report_data=report_data,
                           total_salary=total_salary,
                           teacher_name=teacher_name,
                           selected_teacher=selected_teacher,
                           selected_year=selected_year)

@bp.route('/report/department_salary', methods=['GET', 'POST'])
@login_required
def report_department_salary():
    from ..models.faculties_model import get_faculties
    from ..controllers.classes_controller import get_academic_years

    faculties = get_faculties()
    academic_years = get_academic_years()
    report_data = {}
    selected_faculty = None
    selected_year = None
    if request.method == 'POST':
        selected_faculty = int(request.form['faculty_id'])
        selected_year = request.form['academic_year']
        report_data = report_department_salary_by_year(selected_faculty, selected_year)
    return render_template('report_department_salary.html',
                           faculties=faculties,
                           academic_years=academic_years,
                           report_data=report_data,
                           selected_faculty=selected_faculty,
                           selected_year=selected_year)

@bp.route('/report/school_salary', methods=['GET', 'POST'])
@login_required
def report_school_salary():
    from ..controllers.classes_controller import get_academic_years

    academic_years = get_academic_years()
    report_data = {}
    selected_year = None
    if request.method == 'POST':
        selected_year = request.form['academic_year']
        from ..controllers.teaching_salary_controller import report_school_salary_by_year
        report_data = report_school_salary_by_year(selected_year)
    return render_template('report_school_salary.html',
                           academic_years=academic_years,
                           report_data=report_data,
                           selected_year=selected_year)