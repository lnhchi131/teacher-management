from ..models.teachers_model import get_teachers, get_teacher_by_id, add_teacher, update_teacher, delete_teacher
from ..models.faculties_model import get_faculties
from ..models.degrees_model import get_degrees
import re
from flask import flash

def get_teachers_data():
    from flask import session
    role = session.get('role')
    department_id = session.get('department_id')
    if role == 'department_admin':
        from ..models.teachers_model import get_teachers_by_department
        return get_teachers_by_department(department_id)
    return get_teachers()

def get_teacher_data(teacher_id):
    return get_teacher_by_id(teacher_id)

def get_teacher_by_code(teacher_code):
    from ..models.teachers_model import get_teacher_by_code
    return get_teacher_by_code(teacher_code)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return re.match(r"^\d{10}$", phone)  # 10 số

def is_valid_code(code):
    return re.match(r"^GV\d{3}$", code)

def is_valid_date(date_str):
    try:
        from datetime import datetime
        dob = datetime.strptime(date_str, "%Y-%m-%d")
        now = datetime.now()
        if dob > now or dob.year < 1900:
            return False
        return True
    except:
        return False

def is_valid_full_name(full_name):
    # Cho phép chữ cái, dấu cách, dấu tiếng Việt, tối thiểu 2 ký tự
    return re.match(r"^[A-Za-zÀ-ỹà-ỹ\s]{2,}$", full_name)

def add_teacher_data(form_data):
    code = form_data['code']
    full_name = form_data['full_name']
    dob = form_data['dob']
    phone = form_data['phone']
    email = form_data['email']
    department_id = form_data['department_id']
    degree_id = form_data['degree_id']

    # Kiểm tra mã số trùng
    from ..models.teachers_model import get_teacher_by_code
    if get_teacher_by_code(code):
        flash('Mã số giáo viên đã tồn tại!')
        return False

    # Kiểm tra định dạng
    if not is_valid_code(code):
        flash('Mã số chỉ được chứa chữ cái và số, không dấu, không ký tự đặc biệt!')
        return False
    if not is_valid_email(email):
        flash('Email không hợp lệ!')
        return False
    if not is_valid_phone(phone):
        flash('Số điện thoại không hợp lệ!')
        return False
    if not is_valid_date(dob):
        flash('Ngày sinh không hợp lệ!')
        return False
    if not is_valid_full_name(full_name):
        flash('Họ tên không hợp lệ!')
        return False

    add_teacher(code, full_name, dob, phone, email, department_id, degree_id)
    return True

def update_teacher_data(form_data):
    teacher_id = form_data['teacher_id']
    code = form_data['code']
    full_name = form_data['full_name']
    dob = form_data['dob']
    phone = form_data['phone']
    email = form_data['email']
    department_id = form_data['department_id']
    degree_id = form_data['degree_id']

    # Kiểm tra định dạng
    if not is_valid_code(code):
        flash('Mã số chỉ được chứa chữ cái và số, không dấu, không ký tự đặc biệt!')
        return False
    if not is_valid_email(email):
        flash('Email không hợp lệ!')
        return False
    if not is_valid_phone(phone):
        flash('Số điện thoại không hợp lệ!')
        return False
    if not is_valid_date(dob):
        flash('Ngày sinh không hợp lệ!')
        return False
    if not is_valid_full_name(full_name):
        flash('Họ tên không hợp lệ! Chỉ được chứa chữ cái và dấu cách.')
        return False

    update_teacher(teacher_id, code, full_name, dob, phone, email, department_id, degree_id)
    return True

def delete_teacher_data(teacher_id):
    delete_teacher(teacher_id)
    return True

def get_teacher_form_data():
    return {'departments': get_faculties(), 'degrees': get_degrees()}