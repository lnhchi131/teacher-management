from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.controllers.controller import Controller

bp = Blueprint('main', __name__)
controller = Controller()

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        print("User is already authenticated, redirecting to degrees page")
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Received login attempt: username={username}, password={password}")
        user = controller.verify_user(username, password)
        if user:
            login_user(user)
            print(f"Login successful for user: {username}, is_authenticated: {current_user.is_authenticated}")
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'error')
    
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Đăng xuất thành công!', 'success')
    return redirect(url_for('main.login'))

@bp.route('/')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))
    teachers = controller.get_teachers()
    courses = controller.get_courses()
    classes = controller.get_classes()
    return render_template('index.html', teachers=teachers, courses=courses, classes=classes)

@bp.route('/teachers', methods=['GET', 'POST'])
@login_required
def teachers():
    if request.method == 'POST':
        if 'add_teacher' in request.form:
            teacher_name = request.form['teacher_name']
            birth_date = request.form['birth_date']
            try:
                controller.add_teacher(teacher_name, birth_date)
                flash('Thêm giáo viên thành công!', 'success')
            except Exception as e:
                flash(str(e), 'error')
        elif 'edit_teacher' in request.form:
            teacher_id = int(request.form['teacher_id'])
            teacher_name = request.form['teacher_name']
            birth_date = request.form['birth_date']
            try:
                controller.update_teacher(teacher_id, teacher_name, birth_date)
                flash('Chỉnh sửa giáo viên thành công!', 'success')
            except Exception as e:
                flash(str(e), 'error')
        elif 'delete_teacher' in request.form:
            teacher_id = int(request.form['teacher_id'])
            try:
                controller.delete_teacher(teacher_id)
                flash('Xóa giáo viên thành công!', 'success')
            except Exception as e:
                flash(str(e), 'error')
        return redirect(url_for('main.teachers'))
    
    teachers = controller.get_teachers()
    degrees = controller.get_teachers_with_degrees_info()
    courses = controller.get_courses()
    classes = controller.get_classes()
    return render_template('teachers.html', teachers=teachers, degrees=degrees, courses=courses, classes=classes)

@bp.route('/degrees', methods=['GET', 'POST'])
@login_required
def degrees():
    if request.method == 'POST':
        if 'add_degree' in request.form:
            teacher_id = int(request.form['teacher_id'])
            degree_name = request.form['degree_name']
            try:
                controller.add_degree(degree_name, teacher_id)
                flash('Thêm bằng cấp thành công!', 'success')
            except Exception as e:
                flash(str(e), 'error')
        elif 'edit_degree' in request.form:
            degree_id = int(request.form['degree_id'])
            degree_name = request.form['degree_name']
            try:
                controller.update_degree(degree_id, degree_name)
                flash('Chỉnh sửa bằng cấp thành công!', 'success')
            except Exception as e:
                flash(str(e), 'error')
        return redirect(url_for('main.degrees'))
    
    teachers_with_degrees = controller.get_teachers_with_degrees_info()
    degree_types = ['Thạc sĩ', 'Tiến sĩ', 'Giáo sư']  # Danh sách loại bằng cấp cố định
    return render_template('degrees.html', teachers_with_degrees=teachers_with_degrees, degree_types=degree_types)

@bp.route('/courses', methods=['GET', 'POST'])
@login_required
def courses():
    if request.method == 'POST':
        if 'add' in request.form:
            course_name = request.form['course_name']
            controller.add_course(course_name)
        elif 'delete' in request.form:
            course_id = int(request.form['course_id'])
            controller.delete_course(course_id)
        return redirect(url_for('main.courses'))
    
    courses = controller.get_courses()
    return render_template('courses.html', courses=courses)

@bp.route('/classes', methods=['GET', 'POST'])
@login_required
def classes():
    if request.method == 'POST':
        if 'add' in request.form:
            teacher_id = int(request.form['teacher_id'])
            course_id = int(request.form['course_id'])
            controller.add_class(teacher_id, course_id)
        elif 'delete' in request.form:
            class_id = int(request.form['class_id'])
            controller.delete_class(class_id)
        return redirect(url_for('main.classes'))
    
    teachers = controller.get_teachers()
    courses = controller.get_courses()
    classes = controller.get_classes()
    return render_template('classes.html', teachers=teachers, courses=courses, classes=classes)

@bp.route('/salary')
@login_required
def salary():
    salaries, total_salary = controller.calculate_salary()
    salary_change = 10  # Giả lập thay đổi +10%
    return render_template('salary.html', salaries=salaries, total_salary=int(total_salary), salary_change=salary_change)

@bp.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    if request.method == 'POST':
        details = request.form['details']
        controller.add_report(details)
        return redirect(url_for('main.reports'))
    
    reports = controller.get_reports()
    return render_template('reports.html', reports=reports)