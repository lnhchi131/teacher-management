from ..models.teaching_salary_model import (
    get_teaching_classes, get_teacher_info, get_teaching_rate, get_class_coefficient
)

def calculate_teaching_salary(teacher_id, semester_id):
    classes = get_teaching_classes(teacher_id, semester_id)
    teacher_info = get_teacher_info(teacher_id)
    teaching_rate = get_teaching_rate()
    result = []
    total = 0
    if not teacher_info:
        return [], 0, None
    teacher_name, teacher_coeff, degree_name = teacher_info
    for cl in classes:
        class_id, class_code, course_name, hours, student_count, course_coeff = cl
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
            'tien_lop': tien_lop
        })
        total += tien_lop
    return result, total, teacher_name