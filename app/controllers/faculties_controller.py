from ..models.faculties_model import get_faculties, add_faculty, update_faculty, delete_faculty, get_teachers_by_faculty
import re
from flask import flash

def get_faculties_data():
    faculties = get_faculties()
    faculties_with_teachers = []
    for faculty in faculties:
        teacher_count = get_teachers_by_faculty(faculty[0])
        faculties_with_teachers.append((faculty[0], faculty[1], faculty[2], faculty[3], teacher_count))
    return faculties_with_teachers

def add_faculty_data(form_data):
    code = form_data['code']
    name = form_data['name']
    mission = form_data['mission']
    # Kiểm tra mã khoa trùng
    faculties = get_faculties()
    if any(f[1] == code for f in faculties):
        flash('Mã khoa đã tồn tại!')
        return False
    if not is_valid_faculty_name(name):
        flash('Tên khoa không hợp lệ!')
        return False
    if not is_valid_faculty_code(code):
        flash('Mã khoa không hợp lệ!')
        return False
    add_faculty(code, name, mission)
    return True

def update_faculty_data(form_data):
    faculty_id = form_data['faculty_id']
    code = form_data['code']
    name = form_data['name']
    mission = form_data['mission']
    faculties = get_faculties()
    # Kiểm tra mã khoa trùng (trừ chính mình)
    if any(f[1] == code and str(f[0]) != str(faculty_id) for f in faculties):
        flash('Mã khoa đã tồn tại!')
        return False
    if not is_valid_faculty_code(code):
        flash('Mã khoa không hợp lệ! Chỉ được chứa chữ cái và số, không dấu, không ký tự đặc biệt.')
        return False
    if not is_valid_faculty_name(name):
        flash('Tên khoa không hợp lệ! Chỉ được chứa chữ cái và dấu cách.')
        return False
    update_faculty(faculty_id, code, name, mission)
    return True

def delete_faculty_data(faculty_id):
    teacher_count = get_teachers_by_faculty(faculty_id)
    if teacher_count > 0:
        return False
    delete_faculty(faculty_id)
    return True

def is_valid_faculty_name(name):
    return re.match(r"^[A-Za-zÀ-ỹà-ỹ\s]{2,}$", name)

def is_valid_faculty_code(code):
    return re.match(r"^[A-Za-z0-9]+$", code)