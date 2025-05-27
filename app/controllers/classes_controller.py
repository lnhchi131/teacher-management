from flask import session
from ..models.classes_model import get_courses, add_course, update_course, delete_course, get_classes_by_course
from ..models.classes_model import get_semesters, add_semester, update_semester, delete_semester, get_classes_by_semester
from ..models.classes_model import get_classes, add_class, update_class, delete_class, get_class_stats
from ..models.model import get_db_connection

def get_courses_data():
    department_id = session.get('department_id') if session['role'] == 'department_admin' else None
    return get_courses(department_id)

def add_course_data(form_data):
    code = form_data['code']
    name = form_data['name']
    coefficient = float(form_data['coefficient'])
    department_id = form_data['department_id'] if session['role'] == 'admin' else session.get('department_id')
    add_course(code, name, coefficient, department_id)
    return True

def update_course_data(form_data):
    course_id = form_data['course_id']
    code = form_data['code']
    name = form_data['name']
    coefficient = float(form_data['coefficient'])
    department_id = form_data['department_id'] if session['role'] == 'admin' else session.get('department_id')
    update_course(course_id, code, name, coefficient, department_id)
    return True

def delete_course_data(course_id):
    class_count = get_classes_by_course(course_id)
    if class_count > 0:
        return False
    delete_course(course_id)
    return True

def get_semesters_data():
    return get_semesters()

def add_semester_data(form_data):
    code = form_data['code']
    academic_year = form_data['academic_year']
    start_date = form_data['start_date']
    end_date = form_data['end_date']
    add_semester(code, academic_year, start_date, end_date)
    return True

def update_semester_data(form_data):
    semester_id = form_data['semester_id']
    code = form_data['code']
    academic_year = form_data['academic_year']
    start_date = form_data['start_date']
    end_date = form_data['end_date']
    update_semester(semester_id, code, academic_year, start_date, end_date)
    return True

def delete_semester_data(semester_id):
    class_count = get_classes_by_semester(semester_id)
    if class_count > 0:
        return False
    delete_semester(semester_id)
    return True

def get_classes_data():
    department_id = session.get('department_id') if session['role'] == 'department_admin' else None
    return get_classes(department_id)

def add_class_data(form_data):
    code = form_data['code']
    course_id = form_data['course_id']
    semester_id = form_data['semester_id']
    hours = int(form_data['hours'])
    student_count = int(form_data['student_count'])
    if session['role'] == 'department_admin':
        department_id = session.get('department_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT department_id FROM courses WHERE id = %s", (course_id,))
        course_dept = cursor.fetchone()
        cursor.close()
        conn.close()
        if course_dept and course_dept[0] != department_id:
            return False
    add_class(code, course_id, semester_id, hours, student_count)
    return True

def update_class_data(form_data):
    class_id = form_data['class_id']
    code = form_data['code']
    course_id = form_data['course_id']
    semester_id = form_data['semester_id']
    hours = int(form_data['hours'])
    student_count = int(form_data['student_count'])
    if session['role'] == 'department_admin':
        department_id = session.get('department_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT department_id FROM courses WHERE id = %s", (course_id,))
        course_dept = cursor.fetchone()
        cursor.close()
        conn.close()
        if course_dept and course_dept[0] != department_id:
            return False
    update_class(class_id, code, course_id, semester_id, hours, student_count)
    return True

def delete_class_data(class_id):
    delete_class(class_id)
    return True

def get_class_form_data():
    department_id = session.get('department_id') if session['role'] == 'department_admin' else None
    return {
        'semesters': get_semesters(),
        'courses': get_courses(department_id)
    }

def get_class_stats_data(form_data):
    academic_year = form_data['academic_year']
    department_id = session.get('department_id') if session['role'] == 'department_admin' else None
    return get_class_stats(academic_year, department_id)

def get_academic_years():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT academic_year FROM semesters")
    years = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return years