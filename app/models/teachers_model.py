from .model import get_db_connection

def get_teachers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT t.id, t.code, t.full_name, t.dob, t.phone, t.email, d.name, dg.name "
                   "FROM teachers t JOIN departments d ON t.department_id = d.id "
                   "JOIN degrees dg ON t.degree_id = dg.id")
    teachers = cursor.fetchall()
    cursor.close()
    conn.close()
    return teachers

def get_teacher_by_id(teacher_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT t.id, t.code, t.full_name, t.dob, t.phone, t.email, d.name, dg.name "
                   "FROM teachers t JOIN departments d ON t.department_id = d.id "
                   "JOIN degrees dg ON t.degree_id = dg.id WHERE t.id = %s", (teacher_id,))
    teacher = cursor.fetchone()
    cursor.close()
    conn.close()
    return teacher

def add_teacher(code, full_name, dob, phone, email, department_id, degree_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO teachers (code, full_name, dob, phone, email, department_id, degree_id) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                   (code, full_name, dob, phone, email, department_id, degree_id))
    conn.commit()
    cursor.close()
    conn.close()

def update_teacher(teacher_id, code, full_name, dob, phone, email, department_id, degree_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE teachers SET code = %s, full_name = %s, dob = %s, phone = %s, email = %s, "
                   "department_id = %s, degree_id = %s WHERE id = %s",
                   (code, full_name, dob, phone, email, department_id, degree_id, teacher_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_teacher(teacher_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teachers WHERE id = %s", (teacher_id,))
    conn.commit()
    cursor.close()
    conn.close()