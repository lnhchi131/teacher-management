from flask import flash
from ..models.class_coefficients_model import (
    get_class_coefficients, add_class_coefficient, update_class_coefficient, delete_class_coefficient
)

def get_class_coefficients_data():
    return get_class_coefficients()

def add_class_coefficient_data(form_data):
    min_students = int(form_data['min_students'])
    max_students = int(form_data['max_students'])
    coefficient = float(form_data['coefficient'])
    # Kiểm tra min < max
    if min_students >= max_students:
        flash('Số sinh viên tối thiểu phải nhỏ hơn tối đa!')
        return False
    # Kiểm tra chồng lấn khoảng
    for c in get_class_coefficients():
        if not (max_students < c[1] or min_students > c[2]):
            flash('Khoảng số sinh viên bị chồng lấn với hệ số đã có!')
            return False
    add_class_coefficient(min_students, max_students, coefficient)
    return True

def update_class_coefficient_data(form_data):
    id = int(form_data['id'])
    min_students = int(form_data['min_students'])
    max_students = int(form_data['max_students'])
    coefficient = float(form_data['coefficient'])
    if min_students >= max_students:
        flash('Số sinh viên tối thiểu phải nhỏ hơn tối đa!')
        return False
    # Kiểm tra chồng lấn khoảng (trừ chính mình)
    for c in get_class_coefficients():
        if c[0] != id and not (max_students < c[1] or min_students > c[2]):
            flash('Khoảng số sinh viên bị chồng lấn với hệ số đã có!')
            return False
    update_class_coefficient(id, min_students, max_students, coefficient)
    return True

def delete_class_coefficient_data(id):
    delete_class_coefficient(id)
    return True