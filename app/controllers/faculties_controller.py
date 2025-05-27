from ..models.faculties_model import get_faculties, add_faculty, update_faculty, delete_faculty, get_teachers_by_faculty

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
    add_faculty(code, name, mission)
    return True

def update_faculty_data(form_data):
    faculty_id = form_data['faculty_id']
    code = form_data['code']
    name = form_data['name']
    mission = form_data['mission']
    update_faculty(faculty_id, code, name, mission)
    return True

def delete_faculty_data(faculty_id):
    teacher_count = get_teachers_by_faculty(faculty_id)
    if teacher_count > 0:
        return False
    delete_faculty(faculty_id)
    return True