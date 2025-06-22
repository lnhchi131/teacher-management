from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from ..controllers.teaching_salary_controller import (
    report_teacher_salary_by_year,
    report_department_salary_by_year,
    report_school_salary_by_year
)
from ..models.teachers_model import get_teachers
from ..controllers.classes_controller import get_academic_years
import logging

# Cấu hình logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

bp = Blueprint('teaching_report_routes', __name__)

@bp.route('/report/teacher_salary', methods=['GET', 'POST'])
@login_required
def report_teacher_salary():
    if current_user.role not in ['admin', 'department_admin']:
        flash('Không có quyền truy cập!')
        return redirect('/')
    if current_user.role == 'department_admin':
        from ..models.teachers_model import get_teachers_by_department
        teachers = get_teachers_by_department(current_user.department_id)
    else:
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
        logger.debug(f"Generating report for teacher_id={selected_teacher}, year={selected_year}")
        report_data, total_salary, teacher_name = report_teacher_salary_by_year(selected_teacher, selected_year)
        logger.debug(f"Report data: {report_data}, Total: {total_salary}, Name: {teacher_name}")
        if not report_data:
            flash('Không có dữ liệu lớp học cho giáo viên này trong năm học đã chọn.')
    logger.debug(f"Report data structure: {report_data}")
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
    if current_user.role not in ['admin', 'department_admin']:
        flash('Không có quyền truy cập!')
        return redirect('/')
    from ..models.faculties_model import get_faculties
    from ..controllers.classes_controller import get_academic_years
    from ..controllers.teaching_salary_controller import report_department_salary_by_year

    if current_user.role == 'department_admin':
        faculties = [f for f in get_faculties() if f[0] == current_user.department_id]
    else:
        faculties = get_faculties()
    academic_years = get_academic_years()
    report_data = {}
    total_department_salary = 0
    selected_faculty = None
    selected_year = None

    if request.method == 'POST':
        selected_faculty = int(request.form['faculty_id'])
        selected_year = request.form['academic_year']
        report_data = report_department_salary_by_year(selected_faculty, selected_year)
        total_department_salary = sum(teacher['total_salary'] for teacher in report_data.values())

    return render_template('report_department_salary.html',
                           faculties=faculties,
                           academic_years=academic_years,
                           report_data=report_data,
                           total_department_salary=total_department_salary,
                           selected_faculty=selected_faculty,
                           selected_year=selected_year)

@bp.route('/report/school_salary', methods=['GET', 'POST'])
@login_required
def report_school_salary():
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    
    from ..controllers.classes_controller import get_academic_years
    from ..controllers.teaching_salary_controller import report_school_salary_by_year

    academic_years = get_academic_years()
    report_data = {}
    total_school_salary = 0
    selected_year = None

    if request.method == 'POST':
        selected_year = request.form['academic_year']
        report_data, total_school_salary = report_school_salary_by_year(selected_year)

    return render_template('report_school_salary.html',
                           academic_years=academic_years,
                           report_data=report_data,
                           total_school_salary=total_school_salary,
                           selected_year=selected_year)

def report_department_salary_by_year(department_id, academic_year):
    classes = get_teaching_salary_by_department_and_year(department_id, academic_year)
    teaching_rate = get_teaching_rate()
    result = {}
    for cl in classes:
        teacher_id = cl['teacher_id']
        if teacher_id not in result:
            result[teacher_id] = {'teacher_name': cl['teacher_name'], 'total_salary': 0, 'details': []}
        result[teacher_id]['total_salary'] += cl['tien_lop']
        result[teacher_id]['details'].append(cl)
    return result