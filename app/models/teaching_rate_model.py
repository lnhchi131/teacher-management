from .model import get_db_connection

def get_teaching_rate():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT amount FROM teaching_rate WHERE id=1")
    rate = cursor.fetchone()
    cursor.close()
    conn.close()
    return rate[0] if rate else None

def update_teaching_rate(amount):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE teaching_rate SET amount=%s WHERE id=1", (amount,))
    conn.commit()
    cursor.close()
    conn.close()