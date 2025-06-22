from flask import flash
from ..models.degrees_model import get_degrees, add_degree, update_degree, delete_degree, get_teachers_by_degree
from ..models.teachers_model import get_teachers
import re

def get_degrees_data():
    degrees = get_degrees()
    degrees_with_teachers = []
    for degree in degrees:
        teacher_count = get_teachers_by_degree(degree[0])
        degrees_with_teachers.append((degree[0], degree[1], degree[2], teacher_count))
    return degrees_with_teachers

def add_degree_data(form_data):
    name = form_data['name']
    degrees = get_degrees()
    if any(d[1].strip().lower() == name.strip().lower() for d in degrees):
        flash('Tên bằng cấp đã tồn tại!')
        return False
    if not is_valid_degree_name(name):
        flash('Tên bằng cấp không hợp lệ! Chỉ được chứa chữ cái và dấu cách.')
        return False
    add_degree(name)
    return True

def update_degree_data(form_data):
    degree_id = form_data['degree_id']
    name = form_data['name']
    coefficient = float(form_data['coefficient'])
    degrees = get_degrees()
    if any(d[1].strip().lower() == name.strip().lower() and str(d[0]) != str(degree_id) for d in degrees):
        flash('Tên bằng cấp đã tồn tại!')
        return False
    if not is_valid_degree_name(name):
        flash('Tên bằng cấp không hợp lệ! Chỉ được chứa chữ cái và dấu cách.')
        return False
    update_degree(degree_id, name, coefficient)  # Truyền đủ 3 tham số
    return True

def delete_degree_data(degree_id):
    teacher_count = get_teachers_by_degree(degree_id)
    if teacher_count > 0:
        return False
    delete_degree(degree_id)
    return True

def is_valid_degree_name(name):
    # Chỉ cho phép chữ cái, dấu cách, dấu tiếng Việt, tối thiểu 2 ký tự
    return re.match(r"^[A-Za-zÀ-ỹà-ỹ\s]{2,}$", name)