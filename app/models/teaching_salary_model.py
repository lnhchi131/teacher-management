from .model import get_db_connection
from .class_coefficients_model import get_coefficient_by_student_count

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

def get_teaching_classes(teacher_id, semester_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cl.id, cl.code, co.name, cl.hours, cl.student_count, co.coefficient
        FROM classes cl
        JOIN courses co ON cl.course_id = co.id
        WHERE cl.semester_id = %s AND cl.id IN (
            SELECT id FROM classes WHERE cl.id = id AND cl.semester_id = %s AND cl.course_id = co.id
        )
    """, (semester_id, semester_id))
    classes = cursor.fetchall()
    cursor.close()
    conn.close()
    return classes

def get_teacher_info(teacher_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.full_name, d.coefficient, d.name
        FROM teachers t
        JOIN degrees d ON t.degree_id = d.id
        WHERE t.id = %s
    """, (teacher_id,))
    info = cursor.fetchone()
    cursor.close()
    conn.close()
    return info

def get_teaching_rate():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT amount FROM teaching_rate WHERE id=1")
    rate = cursor.fetchone()
    cursor.close()
    conn.close()
    return rate[0] if rate else 0

def get_class_coefficient(student_count):
    return get_coefficient_by_student_count(student_count)