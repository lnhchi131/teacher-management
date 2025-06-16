from .model import get_db_connection

def get_class_coefficients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, min_students, max_students, coefficient FROM class_coefficients ORDER BY min_students")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def add_class_coefficient(min_students, max_students, coefficient):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO class_coefficients (min_students, max_students, coefficient) VALUES (%s, %s, %s)",
                   (min_students, max_students, coefficient))
    conn.commit()
    cursor.close()
    conn.close()

def update_class_coefficient(id, min_students, max_students, coefficient):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE class_coefficients SET min_students=%s, max_students=%s, coefficient=%s WHERE id=%s",
                   (min_students, max_students, coefficient, id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_class_coefficient(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM class_coefficients WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_coefficient_by_student_count(student_count):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT coefficient FROM class_coefficients WHERE %s BETWEEN min_students AND max_students LIMIT 1",
        (student_count,)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0