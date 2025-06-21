from flask_login import current_user
from ..models.teaching_salary_model import get_teaching_classes, get_teaching_rate, get_class_coefficient, get_teaching_salary_by_teacher_and_year, get_teaching_salary_by_department_and_year, get_teaching_salary_by_school_and_year
from ..models.teachers_model import get_teacher_by_id
import logging

# Cấu hình logging để debug
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def calculate_teaching_salary(teacher_id=None, department_id=None, academic_year=None, semester_id=None):
    logger.debug(f"Input parameters: teacher_id={teacher_id}, department_id={department_id}, "
                 f"academic_year={academic_year}, semester_id={semester_id}")
    # Lấy danh sách lớp đã phân công
    classes = get_teaching_classes(teacher_id, department_id, academic_year, semester_id)
    logger.debug(f"Classes from get_teaching_classes: {classes}")
    if not classes and teacher_id:
        logger.warning("No classes found for teacher_id with given filters")
        return [], 0, None

    teaching_rate = get_teaching_rate()
    logger.debug(f"Teaching rate: {teaching_rate}")
    result = []
    total = 0
    teacher_name = None

    # Lấy thông tin giáo viên
    teacher_info = get_teacher_by_id(teacher_id) if teacher_id else None
    if teacher_info:
        _, _, teacher_name, _, _, _, dep_name, degree_name = teacher_info
        teacher_coeff = next((d[2] for d in get_degrees() if d[1] == degree_name), 1.0)
        logger.debug(f"Teacher info: name={teacher_name}, coeff={teacher_coeff}, degree={degree_name}")
    else:
        teacher_coeff = 1.0
        logger.warning("No teacher info found, using default coefficient 1.0")

    for cl in classes:
        class_id, class_code, course_name, hours, student_count, course_coeff, \
        t_id, t_name, teacher_coeff_from_db, degree_name_from_db, dep_id, dep_name, academic_year = cl
        class_coeff = get_class_coefficient(student_count)
        logger.debug(f"Class data: code={class_code}, hours={hours}, student_count={student_count}, "
                     f"coeffs={course_coeff}+{class_coeff}")
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
            'degree_name': degree_name_from_db,
            'department_id': dep_id,
            'department_name': dep_name,
            'academic_year': academic_year
        })
        total += tien_lop
        logger.debug(f"Class {class_code} salary: {tien_lop}")

    logger.debug(f"Total salary: {total}")
    return result, total, teacher_name

def report_teacher_salary_by_year(teacher_id, academic_year):
    classes = get_teaching_salary_by_teacher_and_year(teacher_id, academic_year)
    teaching_rate = get_teaching_rate()
    result = []
    total = 0
    teacher_name = None
    teacher_info = get_teacher_by_id(teacher_id)
    if teacher_info:
        _, _, teacher_name, _, _, _, dep_name, degree_name = teacher_info
        teacher_coeff = next((d[2] for d in get_degrees() if d[1] == degree_name), 1.0)
    else:
        teacher_coeff = 1.0

    for cl in classes:
        class_id, class_code, course_name, hours, student_count, course_coeff, \
        t_id, t_name, teacher_coeff_from_db, degree_name_from_db, dep_id, dep_name, academic_year = cl
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
    return result, total, teacher_name

def report_department_salary_by_year(department_id, academic_year):
    classes = get_teaching_salary_by_department_and_year(department_id, academic_year)
    teaching_rate = get_teaching_rate()
    result = {}
    for cl in classes:
        class_id, class_code, course_name, hours, student_count, course_coeff, \
        t_id, t_name, teacher_coeff_from_db, degree_name_from_db, dep_id, dep_name, academic_year = cl
        class_coeff = get_class_coefficient(student_count)
        so_tiet_quy_doi = hours * (course_coeff + class_coeff)
        tien_lop = so_tiet_quy_doi * teacher_coeff_from_db * teaching_rate
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
        t_id, t_name, teacher_coeff_from_db, degree_name_from_db, dep_id, dep_name, academic_year = cl
        class_coeff = get_class_coefficient(student_count)
        so_tiet_quy_doi = hours * (course_coeff + class_coeff)
        tien_lop = so_tiet_quy_doi * teacher_coeff_from_db * teaching_rate
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

# Hàm phụ trợ
def get_teacher_department(teacher_id):
    from ..models.teachers_model import get_teacher_by_id
    teacher = get_teacher_by_id(teacher_id)
    return teacher[5] if teacher and len(teacher) > 5 else None  # department_id (index 5)

def get_degrees():
    from ..models.degrees_model import get_degrees
    return get_degrees()
