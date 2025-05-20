import mysql.connector
from mysql.connector import Error
from mysql.connector.pooling import MySQLConnectionPool
import time

# Khởi tạo connection pool
pool_config = {
    "pool_name": "teacher_management_pool",
    "pool_size": 10,
    "host": "mysql-34fa5599-scvgden-9e65.b.aivencloud.com",
    "port": 10023,
    "user": "avnadmin",
    "password": "AVNS_OeD2WJJNW4UHZZOtCEi",
    "database": "teacher_management",
    "ssl_ca": None,
    "ssl_verify_cert": False
}

connection_pool = MySQLConnectionPool(**pool_config)

class User:
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False

    def get_id(self):
        return str(self.id)

class Model:
    def __init__(self):
        pass

    def _get_connection(self, retries=3, delay=1):
        """Lấy kết nối từ pool với cơ chế thử lại."""
        for attempt in range(retries):
            try:
                connection = connection_pool.get_connection()
                if not connection.is_connected():
                    connection.reconnect()
                return connection
            except Error as e:
                if attempt < retries - 1:
                    time.sleep(delay)
                    continue
                print(f"Error getting connection from pool: {e}")
                raise Exception("Failed to get database connection from pool.")

    def get_user_by_username(self, username):
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            if user:
                print(f"User found: id={user[0]}, username={user[1]}, password={user[2]}")
                return {'id': user[0], 'username': user[1], 'password': user[2]}
            print(f"User not found for username: {username}")
            return None

    def get_user_by_username_by_id(self, user_id):
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, username FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            cursor.close()
            if user:
                print(f"User found: id={user[0]}, username={user[1]}")
                return {'id': user[0], 'username': user[1]}
            print(f"User not found for user_id: {user_id}")
            return None

    def verify_user(self, username, password):
        user = self.get_user_by_username(username)
        if user and user['password'] == password:
            print("Password verification successful")
            return User(user['id'], user['username'])
        print("Password verification failed")
        return None

    def add_teacher(self, code, full_name, birth_date, phone, email):
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO teachers (code, name, birth_date, phone, email) VALUES (%s, %s, %s, %s, %s)",
                (code, full_name, birth_date, phone, email)
            )
            connection.commit()
            teacher_id = cursor.lastrowid
            cursor.close()
            return teacher_id

    def update_teacher(self, teacher_id, code, full_name, birth_date, phone, email):
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE teachers SET code = %s, name = %s, birth_date = %s, phone = %s, email = %s WHERE id = %s",
                (code, full_name, birth_date, phone, email, teacher_id)
            )
            connection.commit()
            cursor.close()

    def delete_teacher(self, teacher_id):
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM classes WHERE teacher_id = %s", (teacher_id,))
            cursor.execute("DELETE FROM degrees WHERE teacher_id = %s", (teacher_id,))
            cursor.execute("DELETE FROM teachers WHERE id = %s", (teacher_id,))
            connection.commit()
            cursor.close()

    def add_degree(self, degree_name, teacher_id):
        with self._get_connection() as connection:
            cursor = connection.cursor()
            try:
                cursor.execute("INSERT INTO degrees (name, teacher_id) VALUES (%s, %s)", (degree_name, teacher_id))
                connection.commit()
            except mysql.connector.Error as e:
                if e.errno == 1062:  # Duplicate entry error (UNIQUE constraint)
                    raise Exception("Giáo viên này đã có bằng cấp. Mỗi giáo viên chỉ có thể có một bằng cấp.")
                raise e
            finally:
                cursor.close()

    def update_degree(self, degree_id, degree_name):
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE degrees SET name = %s WHERE id = %s", (degree_name, degree_id))
            connection.commit()
            cursor.close()

    def get_teachers_with_degrees_info(self):
        with self._get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT t.id, t.name, d.id as degree_id, d.name as degree_name 
                FROM teachers t 
                LEFT JOIN degrees d ON t.id = d.teacher_id
            """)
            teachers_with_degrees = cursor.fetchall()
            cursor.close()
            return teachers_with_degrees

    def delete_degree(self, teacher_id):
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM degrees WHERE teacher_id = %s", (teacher_id,))
            connection.commit()
            cursor.close()

    def add_faculty(self, name, abbreviation, description=None):
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO faculty (name, abbreviation, description) VALUES (%s, %s, %s)", (name, abbreviation, description))
            connection.commit()
            cursor.close()

    def get_faculties(self):
        with self._get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, name, abbreviation, description FROM faculty")
            faculties = cursor.fetchall()
            cursor.close()
            return faculties

    def update_faculty(self, faculty_id, name, abbreviation, description=None):
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE faculty SET name = %s, abbreviation = %s, description = %s WHERE id = %s", 
                           (name, abbreviation, description, faculty_id))
            connection.commit()
            cursor.close()

    def delete_faculty(self, faculty_id):
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM classes WHERE faculty_id = %s", (faculty_id,))
            cursor.execute("DELETE FROM faculty WHERE id = %s", (faculty_id,))
            connection.commit()
            cursor.close()

    def get_teachers(self):
        with self._get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, code, name, birth_date, phone, email FROM teachers")
            teachers = cursor.fetchall()
            cursor.close()
            return teachers

    def get_teachers_with_degrees(self):
        with self._get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT t.id, t.name, d.name as degree_name
                FROM teachers t
                LEFT JOIN degrees d ON t.id = d.teacher_id
            """)
            teachers = cursor.fetchall()
            cursor.close()
            return teachers

    def get_class_count_by_teacher(self, teacher_id):
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM classes WHERE teacher_id = %s", (teacher_id,))
            count = cursor.fetchone()[0]
            cursor.close()
            return count

    def add_class(self, teacher_id, faculty_id):
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO classes (teacher_id, faculty_id) VALUES (%s, %s)", (teacher_id, faculty_id))
            connection.commit()
            cursor.close()

    def get_classes(self):
        with self._get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT c.id, t.name as teacher_name, f.name as faculty_name
                FROM classes c
                JOIN teachers t ON c.teacher_id = t.id
                JOIN faculty f ON c.faculty_id = f.id
            """)
            classes = cursor.fetchall()
            cursor.close()
            return classes

    def delete_class(self, class_id):
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM classes WHERE id = %s", (class_id,))
            connection.commit()
            cursor.close()

    def add_report(self, details):
        with self._get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO reports (details) VALUES (%s)", (details,))
            connection.commit()
            cursor.close()

    def get_reports(self):
        with self._get_connection() as connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, details FROM reports")
            reports = cursor.fetchall()
            cursor.close()
            return reports