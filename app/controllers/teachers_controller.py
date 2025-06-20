from ..models.teachers_model import get_teachers, get_teacher_by_id, add_teacher, update_teacher, delete_teacher
from ..models.faculties_model import get_faculties
from ..models.degrees_model import get_degrees

def get_teachers_data():
    return get_teachers()

def get_teacher_data(teacher_id):
    return get_teacher_by_id(teacher_id)

def get_teacher_by_code(teacher_code):
    from ..models.teachers_model import get_teacher_by_code
    return get_teacher_by_code(teacher_code)

def add_teacher_data(form_data):
    code = form_data['code']
    full_name = form_data['full_name']
    dob = form_data['dob']
    phone = form_data['phone']
    email = form_data['email']
    department_id = form_data['department_id']
    degree_id = form_data['degree_id']
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
    update_teacher(teacher_id, code, full_name, dob, phone, email, department_id, degree_id)
    return True

def delete_teacher_data(teacher_id):
    delete_teacher(teacher_id)
    return True

def get_teacher_form_data():
    return {'departments': get_faculties(), 'degrees': get_degrees()}