from ..models.degrees_model import get_degrees, add_degree, update_degree, delete_degree, get_teachers_by_degree
from ..models.teachers_model import get_teachers

def get_degrees_data():
    degrees = get_degrees()
    degrees_with_teachers = []
    for degree in degrees:
        teacher_count = get_teachers_by_degree(degree[0])
        degrees_with_teachers.append((degree[0], degree[1], degree[2], teacher_count))
    return degrees_with_teachers

def add_degree_data(form_data):
    name = form_data['name']
    coefficient = float(form_data['coefficient'])
    add_degree(name, coefficient)
    return True

def update_degree_data(form_data):
    degree_id = form_data['degree_id']
    name = form_data['name']
    coefficient = float(form_data['coefficient'])
    update_degree(degree_id, name, coefficient)
    return True

def delete_degree_data(degree_id):
    teacher_count = get_teachers_by_degree(degree_id)
    if teacher_count > 0:
        return False
    delete_degree(degree_id)
    return True