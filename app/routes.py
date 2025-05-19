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
    faculty = controller.get_faculty()
    classes = controller.get_classes()
    salaries, total_salary = controller.calculate_salary()
    return render_template('index.html', teachers=teachers, faculty=faculty, classes=classes, total_salary=total_salary)

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
    
    search = request.args.get('search', '').strip()
    teachers = controller.get_teachers()
    if search:
        teachers = [t for t in teachers if search.lower() in str(t[0]).lower() or search.lower() in t[1].lower()]
        
    degrees = controller.get_teachers_with_degrees_info()
    faculty = controller.get_faculty()
    classes = controller.get_classes()
    return render_template('teachers.html', teachers=teachers, degrees=degrees, faculty=faculty, classes=classes)

@bp.route('/degrees', methods=['GET', 'POST'])
@login_required
def degrees():
    teachers_with_degrees = controller.get_teachers_with_degrees_info()
    degree_types = ['Thạc sĩ', 'Tiến sĩ', 'Phó Giáo Sư', 'Giáo sư']
    edit_degree = None
    message = None

    if request.method == 'POST':
        if 'edit_id' in request.form:  # Khi ấn nút Sửa
            edit_id = int(request.form['edit_id'])
            for teacher in teachers_with_degrees:
                if teacher[2] == edit_id:  # Tìm bằng cấp cần sửa
                    edit_degree = {
                        'id': teacher[2],
                        'name': teacher[3],
                        'teacher_id': teacher[0],
                        'teacher_name': teacher[1]
                    }
                    break
        elif 'save_edit' in request.form:  # Khi lưu thay đổi
            degree_id = int(request.form['degree_id'])
            degree_name = request.form['degree_name']
            try:
                controller.update_degree(degree_id, degree_name)
                message = "Cập nhật bằng cấp thành công!"
            except Exception as e:
                message = str(e)
            return redirect(url_for('main.degrees'))

    return render_template(
        'degrees.html',
        teachers_with_degrees=teachers_with_degrees,
        degree_types=degree_types,
        edit_degree=edit_degree,
        message=message
    )

@bp.route('/faculty', methods=['GET', 'POST'])
@login_required
def faculty():
    faculties = controller.get_faculty()
    edit_faculty = None
    message = None

    if request.method == 'POST':
        if 'edit_id' in request.form:  # Khi ấn nút Sửa
            edit_id = int(request.form['edit_id'])
            for faculty in faculties:
                if faculty['id'] == edit_id:
                    edit_faculty = faculty
                    break
        elif 'save_edit' in request.form:  # Khi lưu thay đổi
            faculty_id = int(request.form['faculty_id'])
            name = request.form['name']
            abbreviation = request.form['abbreviation']
            description = request.form['description']
            controller.update_faculty(faculty_id, name, abbreviation, description)
            message = "Cập nhật thông tin khoa thành công!"
            return redirect(url_for('main.faculty'))

    return render_template('faculty.html', faculties=faculties, edit_faculty=edit_faculty, message=message)

@bp.route('/faculty/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_faculty(id):
    faculties = controller.get_faculty()
    # Tìm faculty cần sửa
    edit_faculty = None
    for fac in faculties:
        if fac[0] == id or getattr(fac, 'id', None) == id:
            # Nếu là tuple (id, name), bạn cần lấy đúng thông tin
            edit_faculty = {
                'id': fac[0],
                'name': fac[1],
                'abbreviation': getattr(fac, 'abbreviation', ''),
                'description': getattr(fac, 'description', '')
            }
            break

    if request.method == 'POST':
        name = request.form['name']
        abbreviation = request.form.get('abbreviation', '')
        description = request.form.get('description', '')
        # Bạn cần viết hàm update_faculty trong controller và model
        controller.update_faculty(id, name, abbreviation, description)
        return redirect(url_for('main.faculty'))

    return render_template('faculty.html', faculties=faculties, edit_faculty=edit_faculty)

@bp.route('/classes', methods=['GET', 'POST'])
@login_required
def classes():
    if request.method == 'POST':
        if 'add' in request.form:
            teacher_id = int(request.form['teacher_id'])
            faculty_id = int(request.form['faculty_id'])
            controller.add_class(teacher_id, faculty_id)
        elif 'delete' in request.form:
            class_id = int(request.form['class_id'])
            controller.delete_class(class_id)
        return redirect(url_for('main.classes'))
    
    teachers = controller.get_teachers()
    faculty = controller.get_faculty()
    classes = controller.get_classes()
    return render_template('classes.html', teachers=teachers, faculty=faculty, classes=classes)

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

@bp.route('/faculty/delete/<int:id>', methods=['GET'])
@login_required
def delete_faculty(id):
    controller.delete_faculty(id)
    return redirect(url_for('main.faculty'))