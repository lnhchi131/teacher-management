import re
from flask import session, flash
from ..models.classes_model import (
    get_courses, add_course, update_course, delete_course, get_classes_by_course,
    get_semesters, add_semester, update_semester, delete_semester, get_classes_by_semester,
    get_classes, add_class, update_class, delete_class, get_class_stats,
    get_teachers, get_assigned_classes, assign_class, remove_assignment, get_unassigned_classes
)
from ..models.model import get_db_connection

def is_valid_course_code(code):
    # Chỉ cho phép chữ cái và số, không dấu, không ký tự đặc biệt
    return re.match(r"^[A-Za-z0-9]+$", code)

def is_valid_course_name(name):
    # Chỉ cho phép chữ cái, dấu cách, dấu tiếng Việt, tối thiểu 2 ký tự
    return re.match(r"^[A-Za-zÀ-ỹà-ỹ\s]{2,}$", name)

def is_valid_class_code(code):
    # Định dạng: chữ/số, có thể có dấu gạch ngang, ví dụ: CS101-01
    return re.match(r"^[A-Za-z0-9\-]+$", code)

def is_valid_class_name(name):
    # Nếu có trường tên lớp, chỉ cho phép chữ cái, dấu cách, dấu tiếng Việt, tối thiểu 2 ký tự
    return re.match(r"^[A-Za-zÀ-ỹà-ỹ\s]{2,}$", name)

def is_valid_semester_code(code):
    # Chỉ cho phép chữ cái và số, không dấu, không ký tự đặc biệt
    return re.match(r"^[A-Za-z0-9]+$", code)

def is_valid_academic_year(year):
    # Định dạng: 4 số - 4 số, ví dụ: 2024-2025
    return re.match(r"^\d{4}-\d{4}$", year)

def get_courses_data():
    role = session.get('role')
    department_id = session.get('department_id') if role == 'department_admin' else None
    return get_courses(department_id)

def add_course_data(form_data):
    code = form_data['code']
    name = form_data['name']
    coefficient = float(form_data['coefficient'])
    role = session.get('role')
    department_id = form_data['department_id'] if role == 'admin' else session.get('department_id')
    courses = get_courses()
    if any(c[1] == code for c in courses):
        flash('Mã học phần đã tồn tại!')
        return False
    if not is_valid_course_code(code):
        flash('Mã học phần không hợp lệ! Chỉ được chứa chữ cái và số.')
        return False
    if not is_valid_course_name(name):
        flash('Tên học phần không hợp lệ! Chỉ được chứa chữ cái và dấu cách.')
        return False
    add_course(code, name, coefficient, department_id)
    return True

def update_course_data(form_data):
    course_id = form_data['course_id']
    code = form_data['code']
    name = form_data['name']
    coefficient = float(form_data['coefficient'])
    role = session.get('role')
    department_id = form_data['department_id'] if role == 'admin' else session.get('department_id')
    courses = get_courses()
    if any(c[1] == code and str(c[0]) != str(course_id) for c in courses):
        flash('Mã học phần đã tồn tại!')
        return False
    if not is_valid_course_code(code):
        flash('Mã học phần không hợp lệ! Chỉ được chứa chữ cái và số.')
        return False
    if not is_valid_course_name(name):
        flash('Tên học phần không hợp lệ! Chỉ được chứa chữ cái và dấu cách.')
        return False
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
    semesters = get_semesters()
    if any(s[1] == code for s in semesters):
        flash('Mã kỳ học đã tồn tại!')
        return False
    if not is_valid_semester_code(code):
        flash('Mã kỳ học không hợp lệ! Chỉ được chứa chữ cái và số.')
        return False
    if not is_valid_academic_year(academic_year):
        flash('Năm học không hợp lệ! Định dạng phải là YYYY-YYYY.')
        return False
    add_semester(code, academic_year, start_date, end_date)
    return True

def update_semester_data(form_data):
    semester_id = form_data['semester_id']
    code = form_data['code']
    academic_year = form_data['academic_year']
    start_date = form_data['start_date']
    end_date = form_data['end_date']
    semesters = get_semesters()
    if any(s[1] == code and str(s[0]) != str(semester_id) for s in semesters):
        flash('Mã kỳ học đã tồn tại!')
        return False
    if not is_valid_semester_code(code):
        flash('Mã kỳ học không hợp lệ! Chỉ được chứa chữ cái và số.')
        return False
    if not is_valid_academic_year(academic_year):
        flash('Năm học không hợp lệ! Định dạng phải là YYYY-YYYY.')
        return False
    update_semester(semester_id, code, academic_year, start_date, end_date)
    return True

def delete_semester_data(semester_id):
    class_count = get_classes_by_semester(semester_id)
    if class_count > 0:
        return False
    delete_semester(semester_id)
    return True

def get_classes_data():
    role = session.get('role')
    department_id = session.get('department_id') if role == 'department_admin' else None
    return get_classes(department_id)

def add_class_data(form_data):
    code = form_data['code']
    classes = get_classes()
    if any(c[1] == code for c in classes):
        flash('Mã lớp đã tồn tại!')
        return False
    if not is_valid_class_code(code):
        flash('Mã lớp không hợp lệ! Chỉ được chứa chữ cái, số, dấu gạch ngang, không dấu tiếng Việt, không ký tự đặc biệt.')
        return False
    # Nếu có trường tên lớp:
    # name = form_data['name']
    # if not is_valid_class_name(name):
    #     flash('Tên lớp không hợp lệ! Chỉ được chứa chữ cái và dấu cách.')
    #     return False

    course_id = form_data['course_id']
    semester_id = form_data['semester_id']
    hours = int(form_data['hours'])
    student_count = int(form_data['student_count'])
    role = session.get('role')
    if role == 'department_admin':
        department_id = session.get('department_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT department_id FROM courses WHERE id = %s", (course_id,))
        course_dept = cursor.fetchone()
        cursor.close()
        conn.close()
        if course_dept and course_dept[0] != department_id:
            flash('Bạn chỉ được thêm lớp cho học phần thuộc khoa của mình!')
            return False
    add_class(code, course_id, semester_id, hours, student_count)
    return True

def update_class_data(form_data):
    class_id = form_data['class_id']
    code = form_data['code']
    classes = get_classes()
    if any(c[1] == code and str(c[0]) != str(class_id) for c in classes):
        flash('Mã lớp đã tồn tại!')
        return False
    if not is_valid_class_code(code):
        flash('Mã lớp không hợp lệ! Chỉ được chứa chữ cái, số, dấu gạch ngang, không dấu tiếng Việt, không ký tự đặc biệt.')
        return False
    # Nếu có trường tên lớp:
    # name = form_data['name']
    # if not is_valid_class_name(name):
    #     flash('Tên lớp không hợp lệ! Chỉ được chứa chữ cái và dấu cách.')
    #     return False

        course_id = form_data['course_id']
        semester_id = form_data['semester_id']
        hours = int(form_data['hours'])
        student_count = int(form_data['student_count'])
        role = session.get('role')
    if role == 'department_admin':
        department_id = session.get('department_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT department_id FROM courses WHERE id = %s", (course_id,))
        course_dept = cursor.fetchone()
        cursor.close()
        conn.close()
        if course_dept and course_dept[0] != department_id:
            flash('Bạn chỉ được sửa lớp cho học phần thuộc khoa của mình!')
            return False
    update_class(class_id, code, course_id, semester_id, hours, student_count)
    return True

def delete_class_data(class_id):
    delete_class(class_id)
    return True

def get_class_form_data():
    role = session.get('role')
    department_id = session.get('department_id') if role == 'department_admin' else None
    return {
        'semesters': get_semesters(),
        'courses': get_courses(department_id)
    }

def get_class_stats_data(form_data):
    academic_year = form_data['academic_year']
    role = session.get('role')
    department_id = session.get('department_id') if role == 'department_admin' else None
    return get_class_stats(academic_year, department_id)

def get_academic_years():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT academic_year FROM semesters")
    years = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return years

def get_teachers_data():
    return get_teachers()

def get_assigned_classes_data(teacher_id):
    return get_assigned_classes(teacher_id)

def assign_class_data(form_data):
    teacher_id = form_data['teacher_id']
    class_id = form_data['class_id']
    role = session.get('role')
    if role == 'department_admin':
        department_id = session.get('department_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT department_id FROM courses WHERE id = (SELECT course_id FROM classes WHERE id = %s)", (class_id,))
        course_dept = cursor.fetchone()
        cursor.close()
        conn.close()
        if course_dept and course_dept[0] != department_id:
            return False
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT department_id FROM teachers WHERE id = %s", (teacher_id,))
        teacher_dept = cursor.fetchone()
        cursor.close()
        conn.close()
        if teacher_dept and teacher_dept[0] != department_id:
            return False
    assign_class(teacher_id, class_id)
    return True

def remove_assignment_data(form_data):
    teacher_id = form_data['teacher_id']
    class_id = form_data['class_id']
    role = session.get('role')
    if role == 'department_admin':
        department_id = session.get('department_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT department_id FROM courses WHERE id = (SELECT course_id FROM classes WHERE id = %s)", (class_id,))
        course_dept = cursor.fetchone()
        cursor.close()
        conn.close()
        if course_dept and course_dept[0] != department_id:
            return False
    remove_assignment(teacher_id, class_id)
    return True

def get_unassigned_classes_data():
    role = session.get('role')
    department_id = session.get('department_id') if role == 'department_admin' else None
    return get_unassigned_classes(department_id)