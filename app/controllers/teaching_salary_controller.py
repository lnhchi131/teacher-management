from ..models.teaching_salary_model import (
    get_teaching_classes, get_teaching_rate, get_class_coefficient,
    get_teaching_salary_by_teacher_and_year, get_teaching_salary_by_department_and_year,
    get_teaching_salary_by_school_and_year
)

def calculate_teaching_salary(teacher_id=None, department_id=None, academic_year=None, semester_id=None):
    classes = get_teaching_classes(teacher_id, department_id, academic_year, semester_id)
    teaching_rate = get_teaching_rate()
    result = []
    total = 0
    teacher_name = None
    for cl in classes:
        class_id, class_code, course_name, hours, student_count, course_coeff, \
        t_id, t_name, teacher_coeff, degree_name, dep_id, dep_name, academic_year = cl
        class_coeff = get_class_coefficient(student_count)
        so_tiet_quy_doi = hours * (course_coeff + class_coeff)
        tien_lop = so_tiet_quy_doi * teacher_coeff * teaching_rate
        result.append({
            'class_code': class_code,
            'course_name': course_name,
            'hours': hours,
            'student_count': student_count,
            'course_coeff': course_coeff,
            'class_coeff': class_coeff,
            'so_tiet_quy_doi': so_tiet_quy_doi,
            'tien_lop': tien_lop,
            'teacher_id': t_id,
            'teacher_name': t_name,
            'degree_name': degree_name,
            'department_id': dep_id,
            'department_name': dep_name,
            'academic_year': academic_year
        })
        total += tien_lop
        teacher_name = t_name
    return result, total, teacher_name

def report_teacher_salary_by_year(teacher_id, academic_year):
    classes = get_teaching_salary_by_teacher_and_year(teacher_id, academic_year)
    teaching_rate = get_teaching_rate()
    result = []
    total = 0
    teacher_name = None
    for cl in classes:
        class_id, class_code, course_name, hours, student_count, course_coeff, \
        t_id, t_name, teacher_coeff, degree_name, dep_id, dep_name, academic_year = cl
        class_coeff = get_class_coefficient(student_count)
        so_tiet_quy_doi = hours * (course_coeff + class_coeff)
        tien_lop = so_tiet_quy_doi * teacher_coeff * teaching_rate
        result.append({
            'class_code': class_code,
            'course_name': course_name,
            'hours': hours,
            'student_count': student_count,
            'course_coeff': course_coeff,
            'class_coeff': class_coeff,
            'so_tiet_quy_doi': so_tiet_quy_doi,
            'tien_lop': tien_lop,
        })
        total += tien_lop
        teacher_name = t_name
    return result, total, teacher_name

def report_department_salary_by_year(department_id, academic_year):
    classes = get_teaching_salary_by_department_and_year(department_id, academic_year)
    teaching_rate = get_teaching_rate()
    result = {}
    for cl in classes:
        class_id, class_code, course_name, hours, student_count, course_coeff, \
        t_id, t_name, teacher_coeff, degree_name, dep_id, dep_name, academic_year = cl
        class_coeff = get_class_coefficient(student_count)
        so_tiet_quy_doi = hours * (course_coeff + class_coeff)
        tien_lop = so_tiet_quy_doi * teacher_coeff * teaching_rate
        if t_id not in result:
            result[t_id] = {
                'teacher_name': t_name,
                'total_salary': 0,
                'details': []
            }
        result[t_id]['details'].append({
            'class_code': class_code,
            'course_name': course_name,
            'hours': hours,
            'student_count': student_count,
            'course_coeff': course_coeff,
            'class_coeff': class_coeff,
            'so_tiet_quy_doi': so_tiet_quy_doi,
            'tien_lop': tien_lop,
        })
        result[t_id]['total_salary'] += tien_lop
    return result

def report_school_salary_by_year(academic_year):
    classes = get_teaching_salary_by_school_and_year(academic_year)
    teaching_rate = get_teaching_rate()
    result = {}
    for cl in classes:
        class_id, class_code, course_name, hours, student_count, course_coeff, \
        t_id, t_name, teacher_coeff, degree_name, dep_id, dep_name, academic_year = cl
        class_coeff = get_class_coefficient(student_count)
        so_tiet_quy_doi = hours * (course_coeff + class_coeff)
        tien_lop = so_tiet_quy_doi * teacher_coeff * teaching_rate
        if t_id not in result:
            result[t_id] = {
                'teacher_name': t_name,
                'department_name': dep_name,
                'total_salary': 0,
                'details': []
            }
        result[t_id]['details'].append({
            'class_code': class_code,
            'course_name': course_name,
            'hours': hours,
            'student_count': student_count,
            'course_coeff': course_coeff,
            'class_coeff': class_coeff,
            'so_tiet_quy_doi': so_tiet_quy_doi,
            'tien_lop': tien_lop,
        })
        result[t_id]['total_salary'] += tien_lop
    return result