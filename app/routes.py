from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.controllers.controller import Controller
from flask_paginate import Pagination
from app import cache

bp = Blueprint('main', __name__)
controller = Controller()

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return {"success": True, "message": "Đã đăng nhập"}
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"Received login attempt: username={username}, password={password}")
        user = controller.verify_user(username, password)
        if user:
            login_user(user)
            print(f"Login successful for user: {username}, is_authenticated: {current_user.is_authenticated}")
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return {"success": True, "message": "Đăng nhập thành công!"}
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('main.index'))
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return {"success": False, "message": "Tên đăng nhập hoặc mật khẩu không đúng!"}
            flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'error')
    
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Đăng xuất thành công!', 'success')
    return redirect(url_for('main.login'))

@bp.route('/')
@login_required
def index():
    teachers = controller.get_teachers()
    faculties = controller.get_faculties()
    classes = controller.get_classes()
    return render_template('index.html', teachers=teachers, faculties=faculties, classes=classes)

@bp.route('/teachers', methods=['GET', 'POST'])
@login_required
def teachers():
    edit_teacher = None
    if request.method == 'POST':
        if 'edit_id' in request.form:
            edit_id = int(request.form['edit_id'])
            teachers = controller.get_teachers()
            edit_teacher = next((t for t in teachers if t['id'] == edit_id), None)
        else:
            code = request.form['code']
            full_name = request.form['full_name']
            birth_date = request.form['birth_date']
            phone = request.form['phone']
            email = request.form['email']
            faculty_id = request.form['faculty_id']
            degree_name = request.form['degree_id']
            try:
                teacher_id = controller.add_teacher(code, full_name, birth_date, phone, email)
                if faculty_id:
                    controller.add_class(teacher_id, int(faculty_id))
                if degree_name:
                    controller.add_degree(degree_name, teacher_id)
                flash('Thêm giáo viên thành công!', 'success')
                cache.delete('teachers')
                cache.delete('classes')
            except Exception as e:
                flash(str(e), 'error')
        return redirect(url_for('main.teachers'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    teachers = cache.get('teachers')
    if teachers is None:
        teachers = controller.get_teachers()
        cache.set('teachers', teachers)
    
    start = (page - 1) * per_page
    end = start + per_page
    paginated_teachers = teachers[start:end]
    pagination = Pagination(page=page, per_page=per_page, total=len(teachers), css_framework='bootstrap5')

    degrees = controller.get_teachers_with_degrees_info()
    degree_types = ['Thạc sĩ', 'Tiến sĩ', 'Giáo sư', 'Phó giáo sư', 'Cử nhân']
    
    faculties = cache.get('faculties')
    if faculties is None:
        faculties = controller.get_faculties()
        cache.set('faculties', faculties)

    classes = cache.get('classes')
    if classes is None:
        classes = controller.get_classes()
        cache.set('classes', classes)

    return render_template('teachers.html', teachers=paginated_teachers, degrees=degrees, degree_types=degree_types, faculties=faculties, classes=classes, pagination=pagination, edit_teacher=edit_teacher)

@bp.route('/edit_teacher/<int:id>', methods=['POST'])
@login_required
def edit_teacher(id):
    code = request.form['code']
    full_name = request.form['full_name']
    birth_date = request.form['birth_date']
    phone = request.form['phone']
    email = request.form['email']
    faculty_id = request.form['faculty_id']
    degree_name = request.form['degree_id']
    try:
        controller.update_teacher(id, code, full_name, birth_date, phone, email)
        if faculty_id:
            controller.delete_class_by_teacher(id)
            controller.add_class(id, int(faculty_id))
        if degree_name:
            controller.update_degree(id, degree_name)
        flash('Chỉnh sửa giáo viên thành công!', 'success')
        cache.delete('teachers')
        cache.delete('classes')
    except Exception as e:
        flash(str(e), 'error')
    return redirect(url_for('main.teachers'))

@bp.route('/delete_teacher/<int:id>', methods=['GET'])
@login_required
def delete_teacher(id):
    controller.delete_teacher(id)
    flash('Xóa giáo viên thành công!', 'success')
    cache.delete('teachers')
    cache.delete('classes')
    return redirect(url_for('main.teachers'))

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
                cache.delete('teachers_with_degrees')
            except Exception as e:
                flash(str(e), 'error')
        elif 'edit_degree' in request.form:
            degree_id = int(request.form['degree_id'])
            degree_name = request.form['degree_name']
            try:
                controller.update_degree(degree_id, degree_name)
                flash('Chỉnh sửa bằng cấp thành công!', 'success')
                cache.delete('teachers_with_degrees')
            except Exception as e:
                flash(str(e), 'error')
        return redirect(url_for('main.degrees'))
    
    teachers_with_degrees = cache.get('teachers_with_degrees')
    if teachers_with_degrees is None:
        teachers_with_degrees = controller.get_teachers_with_degrees_info()
        cache.set('teachers_with_degrees', teachers_with_degrees)

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
            edit_faculty = next((f for f in faculties if f['id'] == edit_id), None)
        elif 'save_edit' in request.form:
            faculty_id = int(request.form['faculty_id'])
            faculty_name = request.form['name']
            abbreviation = request.form['abbreviation']
            description = request.form.get('description', None)
            controller.update_faculty(faculty_id, faculty_name, abbreviation, description)
            flash('Chỉnh sửa khoa thành công!', 'success')
            cache.delete('faculties')
            return redirect(url_for('main.faculty'))
        else:
            faculty_name = request.form['name']
            abbreviation = request.form['abbreviation']
            description = request.form.get('description', None)
            controller.add_faculty(faculty_name, abbreviation, description)
            flash('Thêm khoa thành công!', 'success')
            cache.delete('faculties')
            return redirect(url_for('main.faculty'))

    search_query = request.args.get('search', '').strip()
    faculties = cache.get('faculties')
    if faculties is None:
        faculties = controller.get_faculties()
        cache.set('faculties', faculties)
    
    if search_query:
        filtered_faculties = [
            faculty for faculty in faculties
            if search_query.lower() in faculty['name'].lower() or search_query.lower() in faculty['abbreviation'].lower()
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
    cache.delete('faculties')
    return redirect(url_for('main.faculty'))

@bp.route('/classes', methods=['GET', 'POST'])
@login_required
def classes():
    message = None
    if request.method == 'POST':
        if 'add' in request.form:
            name = request.form['name']
            teacher_id = int(request.form['teacher_id'])
            faculty_id = int(request.form['faculty_id'])
            controller.add_class(name, teacher_id, faculty_id)
            flash('Thêm lớp học thành công!', 'success')
            cache.delete('classes')
            return redirect(url_for('main.classes'))
        return redirect(url_for('main.classes'))
    
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search_query = request.args.get('search', '').strip()
    
    classes = cache.get('classes')
    if classes is None:
        classes = controller.get_classes()
        cache.set('classes', classes)

    if search_query:
        filtered_classes = [
            class_ for class_ in classes
            if search_query.lower() in class_['teacher_name'].lower() or search_query.lower() in class_['faculty_name'].lower()
        ]
        if filtered_classes:
            message = f"Đã tìm thấy {len(filtered_classes)} lớp học phù hợp."
        else:
            message = "Không tìm thấy lớp học nào phù hợp."
        classes = filtered_classes

    start = (page - 1) * per_page
    end = start + per_page
    paginated_classes = classes[start:end]
    pagination = Pagination(page=page, per_page=per_page, total=len(classes), css_framework='bootstrap5')

    teachers = cache.get('teachers')
    if teachers is None:
        teachers = controller.get_teachers()
        cache.set('teachers', teachers)

    faculties = cache.get('faculties')
    if faculties is None:
        faculties = controller.get_faculties()
        cache.set('faculties', faculties)

    return render_template('classes.html', teachers=teachers, faculties=faculties, classes=paginated_classes, message=message, pagination=pagination)

@bp.route('/classes/delete/<int:id>', methods=['GET'])
@login_required
def delete_class(id):
    controller.delete_class(id)
    flash('Xóa lớp học thành công!', 'success')
    cache.delete('classes')
    return redirect(url_for('main.classes'))

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