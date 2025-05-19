from app.models.model import Model

class Controller:
    def __init__(self):
        try:
            self.model = Model()
        except Exception as e:
            print(f"Failed to initialize Model: {e}")
            raise

    def verify_user(self, username, password):
        return self.model.verify_user(username, password)

    def get_teachers(self):
        return self.model.get_teachers()

    def add_teacher(self, teacher_name, birth_date):
        return self.model.add_teacher(teacher_name, birth_date)

    def update_teacher(self, teacher_id, teacher_name, birth_date):
        self.model.update_teacher(teacher_id, teacher_name, birth_date)

    def delete_teacher(self, teacher_id):
        self.model.delete_teacher(teacher_id)

    def get_teachers_with_degrees_info(self):
        return self.model.get_teachers_with_degrees_info()

    def add_degree(self, degree_name, teacher_id):
        self.model.add_degree(degree_name, teacher_id)

    def update_degree(self, degree_id, degree_name):
        self.model.update_degree(degree_id, degree_name)

    def delete_degree(self, degree_id):
        self.model.delete_degree(degree_id)

    def get_faculty(self):
        return self.model.get_faculty()

    def add_faculty(self, name, abbreviation, description):
        self.model.add_faculty(name, abbreviation, description)

    def delete_faculty(self, faculty_id):
        self.model.delete_faculty(faculty_id)

    def update_faculty(self, faculty_id, name, abbreviation, description):
        self.model.update_faculty(faculty_id, name, abbreviation, description)

    def calculate_salary(self):
        teachers = self.model.get_teachers_with_degrees()
        salaries = []
        total_salary = 0
        for teacher in teachers:
            teacher_id = teacher[0]
            teacher_name = teacher[1]
            degree_name = teacher[2] if teacher[2] else 'Cử nhân'
            hours = self.model.get_class_count_by_teacher(teacher_id)
            degree_coefficient = {'Cử nhân': 1.0, 'Thạc sĩ': 1.2, 'Tiến sĩ': 1.5}.get(degree_name, 1.0)
            salary_amount = hours * 50000 * degree_coefficient  # 50,000 VNĐ/giờ
            total_salary += salary_amount
            salaries.append({
                'teacher_id': teacher_id,
                'teacher_name': teacher_name,
                'hours': hours,
                'amount': int(salary_amount)
            })
        return salaries, total_salary

    def add_class(self, teacher_id, faculty_id):
        self.model.add_class(teacher_id, faculty_id)

    def get_classes(self):
        return self.model.get_classes()

    def delete_class(self, class_id):
        self.model.delete_class(class_id)

    def add_report(self, details):
        self.model.add_report(details)

    def get_reports(self):
        return self.model.get_reports()