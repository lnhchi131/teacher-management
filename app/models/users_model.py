from flask_login import UserMixin
from .model import get_db_connection

class User(UserMixin):
    def __init__(self, id, username, role, department_id):
        self.id = id
        self.username = username
        self.role = role
        self.department_id = department_id

def get_user_by_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password, role, department_id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return User(user[0], user[1], user[3], user[4]), user[2]
    return None, None

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, role, department_id FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return User(user[0], user[1], user[2], user[3])
    return None