from .model import get_db_connection

def get_degrees():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, coefficient FROM degrees")
    degrees = cursor.fetchall()
    cursor.close()
    conn.close()
    return degrees

def add_degree(name, coefficient):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO degrees (name, coefficient) VALUES (%s, %s)", (name, coefficient))
    conn.commit()
    cursor.close()
    conn.close()

def update_degree(degree_id, name, coefficient):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE degrees SET name = %s, coefficient = %s WHERE id = %s", (name, coefficient, degree_id))
    conn.commit()
    cursor.close()
    conn.close()

def delete_degree(degree_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM degrees WHERE id = %s", (degree_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_teachers_by_degree(degree_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM teachers WHERE degree_id = %s", (degree_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count