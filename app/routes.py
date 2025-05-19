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
    faculties = controller.get_faculties()
    classes = controller.get_classes()
    return render_template('index.html', teachers=teachers, faculties=faculties, classes=classes)

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
    faculties = controller.get_faculties()
    classes = controller.get_classes()
    return render_template('teachers.html', teachers=teachers, degrees=degrees, faculties=faculties, classes=classes)

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
    degree_types = ['Thạc sĩ', 'Tiến sĩ', 'Giáo sư', 'Phó giáo sư', 'Cử nhân']
    return render_template('degrees.html', teachers_with_degrees=teachers_with_degrees, degree_types=degree_types)

@bp.route('/faculty', methods=['GET', 'POST'])
@login_required
def faculty():
    edit_faculty = None
    message = None

    if request.method == 'POST':
        if 'edit_id' in request.form:
            edit_id = int(request.form['edit_id'])
            faculties = controller.get_faculties()
            edit_faculty = next((f for f in faculties if f[0] == edit_id), None)
        elif 'save_edit' in request.form:
            faculty_id = int(request.form['faculty_id'])
            faculty_name = request.form['name']
            abbreviation = request.form['abbreviation']
            description = request.form.get('description', None)
            controller.update_faculty(faculty_id, faculty_name, abbreviation, description)
            flash('Chỉnh sửa khoa thành công!', 'success')
            return redirect(url_for('main.faculty'))
        else:
            faculty_name = request.form['name']
            abbreviation = request.form['abbreviation']
            description = request.form.get('description', None)
            controller.add_faculty(faculty_name, abbreviation, description)
            flash('Thêm khoa thành công!', 'success')
            return redirect(url_for('main.faculty'))

    search_query = request.args.get('search', '').strip()
    faculties = controller.get_faculties()
    
    if search_query:
        filtered_faculties = [
            faculty for faculty in faculties
            if search_query.lower() in faculty[1].lower() or search_query.lower() in faculty[2].lower()
        ]
        if filtered_faculties:
            message = f"Đã tìm thấy {len(filtered_faculties)} khoa phù hợp."
        else:
            message = "Không tìm thấy khoa nào phù hợp."
        faculties = filtered_faculties

    return render_template('faculty.html', faculties=faculties, edit_faculty=edit_faculty, message=message)

@bp.route('/faculty/delete/<int:id>', methods=['GET'])
@login_required
def delete_faculty(id):
    controller.delete_faculty(id)
    flash('Xóa khoa thành công!', 'success')
    return redirect(url_for('main.faculty'))

@bp.route('/classes', methods=['GET', 'POST'])
@login_required
def classes():
    if request.method == 'POST':
        if 'add' in request.form:
            teacher_id = int(request.form['teacher_id'])
            faculty_id = int(request.form['faculty_id'])
            controller.add_class(teacher_id, faculty_id)
            flash('Thêm lớp học thành công!', 'success')
        elif 'delete' in request.form:
            class_id = int(request.form['class_id'])
            controller.delete_class(class_id)
            flash('Xóa lớp học thành công!', 'success')
        return redirect(url_for('main.classes'))
    
    teachers = controller.get_teachers()
    faculties = controller.get_faculties()
    classes = controller.get_classes()
    return render_template('classes.html', teachers=teachers, faculties=faculties, classes=classes)

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
        flash('Thêm báo cáo thành công!', 'success')
        return redirect(url_for('main.reports'))
    
    reports = controller.get_reports()
    return render_template('reports.html', reports=reports)