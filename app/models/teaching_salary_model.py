from .model import get_db_connection
from .class_coefficients_model import get_coefficient_by_student_count

def calculate_teaching_salary(teacher_id=None, semester_id=None):
    classes = get_teaching_classes(teacher_id, semester_id=semester_id)
    teacher_info = get_teacher_info(teacher_id)
    teaching_rate = get_teaching_rate()
    result = []
    total = 0
    if not teacher_info:
        return [], 0, None
    teacher_name, teacher_coeff, degree_name = teacher_info
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
            'tien_lop': tien_lop
        })
        total += tien_lop
    return result, total, teacher_name

def get_teaching_classes(teacher_id=None, department_id=None, academic_year=None, semester_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        SELECT cl.id, cl.code, co.name, cl.hours, cl.student_count, co.coefficient,
               t.id, t.full_name, d.coefficient, d.name, dep.id, dep.name, s.academic_year
        FROM teacher_class_assignments tca
        JOIN classes cl ON tca.class_id = cl.id
        JOIN courses co ON cl.course_id = co.id
        JOIN semesters s ON cl.semester_id = s.id
        JOIN teachers t ON tca.teacher_id = t.id
        JOIN degrees d ON t.degree_id = d.id
        JOIN departments dep ON t.department_id = dep.id
        WHERE 1=1
    """
    params = []
    if teacher_id:
        sql += " AND tca.teacher_id = %s"
        params.append(teacher_id)
    if department_id:
        sql += " AND dep.id = %s"
        params.append(department_id)
    if academic_year:
        sql += " AND s.academic_year = %s"
        params.append(academic_year)
    if semester_id:
        sql += " AND s.id = %s"
        params.append(semester_id)
    cursor.execute(sql, tuple(params))
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

def get_teaching_salary_by_teacher_and_year(teacher_id, academic_year):
    return get_teaching_classes(teacher_id=teacher_id, academic_year=academic_year)

def get_teaching_salary_by_department_and_year(department_id, academic_year):
    return get_teaching_classes(department_id=department_id, academic_year=academic_year)

def get_teaching_salary_by_school_and_year(academic_year):
    return get_teaching_classes(academic_year=academic_year)