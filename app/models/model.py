import mysql.connector
from mysql.connector import Error

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
        self.connection = None
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",  # Thay bằng username MySQL của bạn
                password="Hanbin22@",  # Thay bằng password MySQL của bạn
                database="teacher_management"
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            raise Exception("Failed to connect to the database. Please check MySQL server and connection details.")

    def get_user_by_username(self, username):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        if user:
            print(f"User found: id={user[0]}, username={user[1]}, password={user[2]}")
            return {'id': user[0], 'username': user[1], 'password': user[2]}
        print(f"User not found for username: {username}")
        return None

    def verify_user(self, username, password):
        user = self.get_user_by_username(username)
        if user:
            print(f"Verifying password for user {username}: stored={user['password']}, input={password}")
            if user['password'] == password:
                print("Password verification successful")
                return User(user['id'], user['username'])
            else:
                print("Password verification failed")
        return None

    def add_teacher(self, name, birth_date):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO teachers (name, birth_date) VALUES (%s, %s)", (name, birth_date))
        self.connection.commit()
        teacher_id = cursor.lastrowid
        cursor.close()
        return teacher_id

    def update_teacher(self, teacher_id, name, birth_date):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        cursor.execute("UPDATE teachers SET name = %s, birth_date = %s WHERE id = %s", (name, birth_date, teacher_id))
        self.connection.commit()
        cursor.close()

    def delete_teacher(self, teacher_id):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        # Xóa các bản ghi liên quan trong bảng classes trước
        cursor.execute("DELETE FROM classes WHERE teacher_id = %s", (teacher_id,))
        # Xóa bằng cấp của giáo viên (nếu có)
        cursor.execute("DELETE FROM degrees WHERE teacher_id = %s", (teacher_id,))
        # Xóa giáo viên
        cursor.execute("DELETE FROM teachers WHERE id = %s", (teacher_id,))
        self.connection.commit()
        cursor.close()

    def add_degree(self, name, teacher_id):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        try:
            cursor.execute("INSERT INTO degrees (name, teacher_id) VALUES (%s, %s)", (name, teacher_id))
            self.connection.commit()
        except mysql.connector.Error as e:
            if e.errno == 1062:  # Duplicate entry error (UNIQUE constraint)
                raise Exception("Giáo viên này đã có bằng cấp. Mỗi giáo viên chỉ có thể có một bằng cấp.")
            else:
                raise e
        finally:
            cursor.close()

    def update_degree(self, degree_id, name):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        cursor.execute("UPDATE degrees SET name = %s WHERE id = %s", (name, degree_id))
        self.connection.commit()
        cursor.close()

    def get_teachers_with_degrees_info(self):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        # Lấy tất cả giáo viên, kể cả những người chưa có bằng cấp
        cursor.execute("""
            SELECT t.id, t.name, d.id, d.name 
            FROM teachers t 
            LEFT JOIN degrees d ON t.id = d.teacher_id
        """)
        teachers_with_degrees = cursor.fetchall()
        cursor.close()
        return teachers_with_degrees

    def delete_degree(self, degree_id):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM degrees WHERE id = %s", (degree_id,))
        self.connection.commit()
        cursor.close()

    def add_faculty(self, name, abbreviation, description):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO faculty (name, abbreviation, description) VALUES (%s, %s, %s)", (name, abbreviation, description))
        self.connection.commit()
        cursor.close()

    def get_faculty(self):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT id, name, abbreviation, description FROM faculty")
        faculty = cursor.fetchall()
        cursor.close()
        return faculty

    def delete_faculty(self, faculty_id):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM faculty WHERE id = %s", (faculty_id,))
        self.connection.commit()
        cursor.close()

    def update_faculty(self, faculty_id, name, abbreviation, description):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE faculty SET name = %s, abbreviation = %s, description = %s WHERE id = %s",
            (name, abbreviation, description, faculty_id)
        )
        self.connection.commit()
        cursor.close()

    def get_teachers(self):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name, birth_date FROM teachers")
        teachers = cursor.fetchall()
        cursor.close()
        return teachers

    def get_teachers_with_degrees(self):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT t.id, t.name, d.name
            FROM teachers t
            LEFT JOIN degrees d ON t.id = d.teacher_id
        """)
        teachers = cursor.fetchall()
        cursor.close()
        return teachers

    def get_class_count_by_teacher(self, teacher_id):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM classes WHERE teacher_id = %s", (teacher_id,))
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def add_class(self, teacher_id, faculty_id):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO classes (teacher_id, faculty_id) VALUES (%s, %s)", (teacher_id, faculty_id))
        self.connection.commit()
        cursor.close()

    def get_classes(self):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT c.id, t.name, co.name
            FROM classes c
            JOIN teachers t ON c.teacher_id = t.id
            JOIN faculty co ON c.faculty_id = co.id
        """)
        classes = cursor.fetchall()
        cursor.close()
        return classes

    def delete_class(self, class_id):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM classes WHERE id = %s", (class_id,))
        self.connection.commit()
        cursor.close()

    def add_report(self, details):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO reports (details) VALUES (%s)", (details,))
        self.connection.commit()
        cursor.close()

    def get_reports(self):
        if self.connection is None:
            raise Exception("Database connection is not established.")
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, details FROM reports")
        reports = cursor.fetchall()
        cursor.close()
        return reports

    def __del__(self):
        if self.connection:
            self.connection.close()