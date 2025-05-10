from flask import render_template, request, redirect, url_for, session, flash
from models import db, User, Degree, Faculty, Teacher, Class
from datetime import datetime, timedelta

def register_routes(app):
    @app.route('/')
    def index():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        teacher_count = Teacher.query.count()
        class_count = Class.query.count()
        faculty_count = Faculty.query.count()
        # Tính tổng lương (giả lập, sẽ chính xác hơn ở route /salary)
        total_salary = 0
        for teacher in Teacher.query.all():
            hours = sum(1 for cls in Class.query.filter_by(teacher_id=teacher.id))
            degree_coefficient = {'Cử nhân': 1.0, 'Thạc sĩ': 1.2, 'Tiến sĩ': 1.5}.get(teacher.degree.name if teacher.degree else 'Cử nhân', 1.0)
            total_salary += hours * 50000 * degree_coefficient
        return render_template('index.html', teacher_count=teacher_count, class_count=class_count, faculty_count=faculty_count, total_salary=int(total_salary))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username, password=password).first()
            if user:
                session['user_id'] = user.id
                return redirect(url_for('index'))
            flash("Tên đăng nhập hoặc mật khẩu không đúng", "error")
            return render_template('login.html')
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        return redirect(url_for('login'))

    @app.route('/degree', methods=['GET', 'POST'])
    def degree():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if request.method == 'POST':
            name = request.form['name']
            new_degree = Degree(name=name)
            db.session.add(new_degree)
            db.session.commit()
            flash("Thêm bằng cấp thành công", "success")
            return redirect(url_for('degree'))
        degrees = Degree.query.all()
        return render_template('degree.html', degrees=degrees)

    @app.route('/degree/edit/<int:id>', methods=['GET', 'POST'])
    def edit_degree(id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        degree = Degree.query.get_or_404(id)
        if request.method == 'POST':
            degree.name = request.form['name']
            db.session.commit()
            flash("Sửa bằng cấp thành công", "success")
            return redirect(url_for('degree'))
        return render_template('degree.html', degrees=Degree.query.all(), edit_degree=degree)

    @app.route('/degree/delete/<int:id>')
    def delete_degree(id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        degree = Degree.query.get_or_404(id)
        db.session.delete(degree)
        db.session.commit()
        flash("Xóa bằng cấp thành công", "success")
        return redirect(url_for('degree'))

    @app.route('/faculty', methods=['GET', 'POST'])
    def faculty():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if request.method == 'POST':
            name = request.form['name']
            abbreviation = request.form['abbreviation']
            description = request.form['description']
            new_faculty = Faculty(name=name, abbreviation=abbreviation, description=description)
            db.session.add(new_faculty)
            db.session.commit()
            flash("Thêm khoa thành công", "success")
            return redirect(url_for('faculty'))
        faculties = Faculty.query.all()
        return render_template('faculty.html', faculties=faculties)

    @app.route('/faculty/edit/<int:id>', methods=['GET', 'POST'])
    def edit_faculty(id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        faculty = Faculty.query.get_or_404(id)
        if request.method == 'POST':
            faculty.name = request.form['name']
            faculty.abbreviation = request.form['abbreviation']
            faculty.description = request.form['description']
            db.session.commit()
            flash("Sửa khoa thành công", "success")
            return redirect(url_for('faculty'))
        return render_template('faculty.html', faculties=Faculty.query.all(), edit_faculty=faculty)

    @app.route('/faculty/delete/<int:id>')
    def delete_faculty(id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        faculty = Faculty.query.get_or_404(id)
        db.session.delete(faculty)
        db.session.commit()
        flash("Xóa khoa thành công", "success")
        return redirect(url_for('faculty'))

    @app.route('/teacher', methods=['GET', 'POST'])
    def teacher():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if request.method == 'POST':
            code = request.form['code']
            full_name = request.form['full_name']
            birth_date = request.form['birth_date']
            phone = request.form['phone']
            email = request.form['email']
            faculty_id = request.form['faculty_id']
            degree_id = request.form['degree_id']
            new_teacher = Teacher(
                code=code, full_name=full_name, birth_date=birth_date,
                phone=phone, email=email, faculty_id=faculty_id, degree_id=degree_id
            )
            db.session.add(new_teacher)
            db.session.commit()
            flash("Thêm giáo viên thành công", "success")
            return redirect(url_for('teacher'))
        teachers = Teacher.query.all()
        faculties = Faculty.query.all()
        degrees = Degree.query.all()
        return render_template('teacher.html', teachers=teachers, faculties=faculties, degrees=degrees)

    @app.route('/teacher/edit/<int:id>', methods=['GET', 'POST'])
    def edit_teacher(id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        teacher = Teacher.query.get_or_404(id)
        if request.method == 'POST':
            teacher.code = request.form['code']
            teacher.full_name = request.form['full_name']
            teacher.birth_date = request.form['birth_date']
            teacher.phone = request.form['phone']
            teacher.email = request.form['email']
            teacher.faculty_id = request.form['faculty_id']
            teacher.degree_id = request.form['degree_id']
            db.session.commit()
            flash("Sửa giáo viên thành công", "success")
            return redirect(url_for('teacher'))
        teachers = Teacher.query.all()
        faculties = Faculty.query.all()
        degrees = Degree.query.all()
        return render_template('teacher.html', teachers=teachers, faculties=faculties, degrees=degrees, edit_teacher=teacher)

    @app.route('/teacher/delete/<int:id>')
    def delete_teacher(id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        teacher = Teacher.query.get_or_404(id)
        db.session.delete(teacher)
        db.session.commit()
        flash("Xóa giáo viên thành công", "success")
        return redirect(url_for('teacher'))

    @app.route('/stats')
    def stats():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        faculty_stats = db.session.query(Faculty.name, db.func.count(Teacher.id)).join(Teacher).group_by(Faculty.name).all()
        degree_stats = db.session.query(Degree.name, db.func.count(Teacher.id)).join(Teacher).group_by(Degree.name).all()
        return render_template('stats.html', faculty_stats=faculty_stats, degree_stats=degree_stats)

    @app.route('/class', methods=['GET', 'POST'])
    def class_list():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if request.method == 'POST':
            code = request.form['code']
            name = request.form['name']
            teacher_id = request.form['teacher_id']
            new_class = Class(code=code, name=name, teacher_id=teacher_id)
            db.session.add(new_class)
            db.session.commit()
            flash("Thêm lớp học thành công", "success")
            return redirect(url_for('class_list'))
        classes = Class.query.all()
        teachers = Teacher.query.all()
        return render_template('class.html', classes=classes, teachers=teachers)

    @app.route('/class/edit/<int:id>', methods=['GET', 'POST'])
    def edit_class(id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        class_obj = Class.query.get_or_404(id)
        if request.method == 'POST':
            class_obj.code = request.form['code']
            class_obj.name = request.form['name']
            class_obj.teacher_id = request.form['teacher_id']
            db.session.commit()
            flash("Sửa lớp học thành công", "success")
            return redirect(url_for('class_list'))
        classes = Class.query.all()
        teachers = Teacher.query.all()
        return render_template('class.html', classes=classes, teachers=teachers, edit_class=class_obj)

    @app.route('/class/delete/<int:id>')
    def delete_class(id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        class_obj = Class.query.get_or_404(id)
        db.session.delete(class_obj)
        db.session.commit()
        flash("Xóa lớp học thành công", "success")
        return redirect(url_for('class_list'))

    @app.route('/salary')
    def salary():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        # Giả lập tính lương
        salaries = []
        total_salary = 0
        for teacher in Teacher.query.all():
            hours = sum(1 for cls in Class.query.filter_by(teacher_id=teacher.id))
            degree_coefficient = {'Cử nhân': 1.0, 'Thạc sĩ': 1.2, 'Tiến sĩ': 1.5}.get(teacher.degree.name if teacher.degree else 'Cử nhân', 1.0)
            salary_amount = hours * 50000 * degree_coefficient  # 50,000 VNĐ/giờ
            total_salary += salary_amount
            salaries.append({'teacher': teacher, 'hours': hours, 'amount': int(salary_amount)})
        # Giả lập thay đổi so với tháng trước
        salary_change = 10  # +10%
        return render_template('salary.html', salaries=salaries, total_salary=int(total_salary), salary_change=salary_change)