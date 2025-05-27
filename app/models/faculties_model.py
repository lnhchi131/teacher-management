from .model import get_db_connection

def get_faculties():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, code, name, mission FROM departments")
    faculties = cursor.fetchall()
    cursor.close()
    conn.close()
    return faculties

def add_faculty(code, name, mission):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO departments (code, name, mission) VALUES (%s, %s, %s)", (code, name, mission))
    conn.commit()
    cursor.close()
    conn.close()

def update_faculty(faculty_id, code, name, mission):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE departments SET code = %s, name = %s, mission = %s WHERE id = %s", (code, name, mission, faculty_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_faculty(faculty_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM departments WHERE id = %s", (faculty_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_teachers_by_faculty(faculty_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM teachers WHERE department_id = %s", (faculty_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count