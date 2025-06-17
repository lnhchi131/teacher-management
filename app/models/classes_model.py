from .model import get_db_connection

def get_courses(department_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if department_id:
        cursor.execute("SELECT id, code, name, coefficient FROM courses WHERE department_id = %s", (department_id,))
    else:
        cursor.execute("SELECT id, code, name, coefficient FROM courses")
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return courses

def add_course(code, name, coefficient, department_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO courses (code, name, coefficient, department_id) VALUES (%s, %s, %s, %s)",
                   (code, name, coefficient, department_id))
    conn.commit()
    cursor.close()
    conn.close()

def update_course(course_id, code, name, coefficient, department_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE courses SET code = %s, name = %s, coefficient = %s, department_id = %s WHERE id = %s",
                   (code, name, coefficient, department_id, course_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_course(course_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM courses WHERE id = %s", (course_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_classes_by_course(course_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM classes WHERE course_id = %s", (course_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def get_semesters():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, code, academic_year, start_date, end_date FROM semesters")
    semesters = cursor.fetchall()
    cursor.close()
    conn.close()
    return semesters

def add_semester(code, academic_year, start_date, end_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO semesters (code, academic_year, start_date, end_date) VALUES (%s, %s, %s, %s)",
                   (code, academic_year, start_date, end_date))
    conn.commit()
    cursor.close()
    conn.close()

def update_semester(semester_id, code, academic_year, start_date, end_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE semesters SET code = %s, academic_year = %s, start_date = %s, end_date = %s WHERE id = %s",
                   (code, academic_year, start_date, end_date, semester_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_semester(semester_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM semesters WHERE id = %s", (semester_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_classes_by_semester(semester_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM classes WHERE semester_id = %s", (semester_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def get_classes(department_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if department_id:
        cursor.execute("SELECT c.id, c.code, co.name, s.academic_year, c.hours, c.student_count "
                       "FROM classes c JOIN semesters s ON c.semester_id = s.id "
                       "JOIN courses co ON c.course_id = co.id "
                       "WHERE co.department_id = %s", (department_id,))
    else:
        cursor.execute("SELECT c.id, c.code, co.name, s.academic_year, c.hours, c.student_count "
                       "FROM classes c JOIN semesters s ON c.semester_id = s.id "
                       "JOIN courses co ON c.course_id = co.id")
    classes = cursor.fetchall()
    cursor.close()
    conn.close()
    return classes

def add_class(code, course_id, semester_id, hours, student_count):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO classes (code, course_id, semester_id, hours, student_count) "
                   "VALUES (%s, %s, %s, %s, %s)",
                   (code, course_id, semester_id, hours, student_count))
    conn.commit()
    cursor.close()
    conn.close()

def update_class(class_id, code, course_id, semester_id, hours, student_count):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE classes SET code = %s, course_id = %s, semester_id = %s, hours = %s, student_count = %s WHERE id = %s",
                   (code, course_id, semester_id, hours, student_count, class_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_class(class_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM classes WHERE id = %s", (class_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_class_stats(academic_year, department_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if department_id:
        cursor.execute("SELECT c.id, c.code, c.name, COUNT(cl.id), SUM(cl.hours), SUM(cl.student_count) "
                       "FROM courses c LEFT JOIN classes cl ON c.id = cl.course_id "
                       "JOIN semesters s ON cl.semester_id = s.id "
                       "WHERE s.academic_year = %s AND c.department_id = %s "
                       "GROUP BY c.id, c.code, c.name", (academic_year, department_id))
    else:
        cursor.execute("SELECT c.id, c.code, c.name, COUNT(cl.id), SUM(cl.hours), SUM(cl.student_count) "
                       "FROM courses c LEFT JOIN classes cl ON c.id = cl.course_id "
                       "JOIN semesters s ON cl.semester_id = s.id "
                       "WHERE s.academic_year = %s "
                       "GROUP BY c.id, c.code, c.name", (academic_year,))
    stats = cursor.fetchall()
    cursor.close()
    conn.close()
    return stats

def get_teachers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT t.id, t.code, t.full_name, d.name FROM teachers t JOIN departments d ON t.department_id = d.id")
    teachers = cursor.fetchall()
    cursor.close()
    conn.close()
    return teachers

def get_assigned_classes(teacher_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT c.id, c.code, co.name, s.academic_year, c.hours, c.student_count "
                   "FROM classes c JOIN semesters s ON c.semester_id = s.id "
                   "JOIN courses co ON c.course_id = co.id "
                   "JOIN teacher_class_assignments tca ON c.id = tca.class_id "
                   "WHERE tca.teacher_id = %s", (teacher_id,))
    classes = cursor.fetchall()
    cursor.close()
    conn.close()
    return classes

def assign_class(teacher_id, class_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO teacher_class_assignments (teacher_id, class_id) VALUES (%s, %s)",
                   (teacher_id, class_id))
    conn.commit()
    cursor.close()
    conn.close()

def remove_assignment(teacher_id, class_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teacher_class_assignments WHERE teacher_id = %s AND class_id = %s",
                   (teacher_id, class_id))
    conn.commit()
    cursor.close()
    conn.close()

def get_unassigned_classes(department_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if department_id:
        cursor.execute("SELECT c.id, c.code, co.name, s.academic_year, c.hours, c.student_count "
                       "FROM classes c JOIN semesters s ON c.semester_id = s.id "
                       "JOIN courses co ON c.course_id = co.id "
                       "WHERE c.id NOT IN (SELECT class_id FROM teacher_class_assignments) "
                       "AND co.department_id = %s", (department_id,))
    else:
        cursor.execute("SELECT c.id, c.code, co.name, s.academic_year, c.hours, c.student_count "
                       "FROM classes c JOIN semesters s ON c.semester_id = s.id "
                       "JOIN courses co ON c.course_id = co.id "
                       "WHERE c.id NOT IN (SELECT class_id FROM teacher_class_assignments)")
    classes = cursor.fetchall()
    cursor.close()
    conn.close()
    return classes

def get_class_semester_id(class_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT semester_id FROM classes WHERE id = %s", (class_id,))
    semester_id = cursor.fetchone()
    cursor.close()
    conn.close()
    return semester_id[0] if semester_id else None