from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from ..controllers.classes_controller import get_courses_data, add_course_data, update_course_data, delete_course_data
from ..controllers.classes_controller import get_semesters_data, add_semester_data, update_semester_data, delete_semester_data
from ..controllers.classes_controller import get_classes_data, add_class_data, update_class_data, delete_class_data, get_class_form_data
from ..controllers.classes_controller import get_class_stats_data, get_academic_years, get_teachers_data
from ..controllers.classes_controller import get_assigned_classes_data, assign_class_data, remove_assignment_data, get_unassigned_classes_data
from ..controllers.faculties_controller import get_faculties_data

bp = Blueprint('class_routes', __name__)

@bp.route('/courses')
@login_required
def courses():
    if current_user.role not in ['admin', 'department_admin']:
        flash('Không có quyền truy cập!')
        return redirect('/')
    courses = get_courses_data()
    return render_template('courses.html', courses=courses)

@bp.route('/courses/add', methods=['GET', 'POST'])
@login_required
def courses_add():
    if current_user.role not in ['admin', 'department_admin']:
        flash('Không có quyền truy cập!')
        return redirect('/')
    if request.method == 'POST':
        if add_course_data(request.form):
            flash('Thêm học phần thành công!')
            return redirect('/courses')
        # Nếu lỗi, giữ lại form và hiển thị thông báo lỗi
        departments = get_faculties_data()
        return render_template('courses_form.html', departments=departments, course=request.form)
    departments = get_faculties_data()
    return render_template('courses_form.html', departments=departments)

@bp.route('/courses/edit/<int:course_id>', methods=['GET', 'POST'])
@login_required
def courses_edit(course_id):
    if current_user.role not in ['admin', 'department_admin']:
        flash('Không có quyền truy cập!')
        return redirect('/')
    if request.method == 'POST':
        update_course_data(request.form)
        flash('Cập nhật học phần thành công!')
        return redirect('/courses')
    courses = get_courses_data()
    course = next((c for c in courses if c[0] == course_id), None)
    departments = get_faculties_data()
    return render_template('courses_form.html', course=course, departments=departments)

@bp.route('/courses/delete/<int:course_id>')
@login_required
def courses_delete(course_id):
    if current_user.role not in ['admin', 'department_admin']:
        flash('Không có quyền truy cập!')
        return redirect('/')
    if delete_course_data(course_id):
        flash('Xóa học phần thành công!')
    else:
        flash('Không thể xóa vì học phần đang có lớp học!')
    return redirect('/courses')

@bp.route('/semesters')
@login_required
def semesters():
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    semesters = get_semesters_data()
    return render_template('semesters.html', semesters=semesters)

@bp.route('/semesters/add', methods=['GET', 'POST'])
@login_required
def semesters_add():
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    if request.method == 'POST':
        if add_semester_data(request.form):
            flash('Thêm kỳ học thành công!')
            return redirect('/semesters')
        # Nếu lỗi, giữ lại form và hiển thị thông báo lỗi
        return render_template('semesters_form.html', semester=request.form)
    return render_template('semesters_form.html')

@bp.route('/semesters/edit/<int:semester_id>', methods=['GET', 'POST'])
@login_required
def semesters_edit(semester_id):
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    if request.method == 'POST':
        update_semester_data(request.form)
        flash('Cập nhật kỳ học thành công!')
        return redirect('/semesters')
    semesters = get_semesters_data()
    semester = next((s for s in semesters if s[0] == semester_id), None)
    return render_template('semesters_form.html', semester=semester)

@bp.route('/semesters/delete/<int:semester_id>')
@login_required
def semesters_delete(semester_id):
    if current_user.role != 'admin':
        flash('Không có quyền truy cập!')
        return redirect('/')
    if delete_semester_data(semester_id):
        flash('Xóa kỳ học thành công!')
    else:
        flash('Không thể xóa vì kỳ học đang có lớp học!')
    return redirect('/semesters')

@bp.route('/classes')
@login_required
def classes():
    if current_user.role not in ['admin', 'department_admin']:
        flash('Không có quyền truy cập!')
        return redirect('/')
    classes = get_classes_data()
    return render_template('classes.html', classes=classes)

@bp.route('/classes/add', methods=['GET', 'POST'])
@login_required
def classes_add():
    if current_user.role not in ['admin', 'department_admin']:
        flash('Không có quyền truy cập!')
        return redirect('/')
    if request.method == 'POST':
        if add_class_data(request.form):
            flash('Thêm lớp học thành công!')
        else:
            flash('Bạn không có quyền thêm lớp học cho học phần này!')
        return redirect('/classes')
    form_data = get_class_form_data()
    return render_template('classes_form.html', semesters=form_data['semesters'], courses=form_data['courses'])

@bp.route('/classes/edit/<int:class_id>', methods=['GET', 'POST'])
@login_required
def classes_edit(class_id):
    if current_user.role not in ['admin', 'department_admin']:
        flash('Không có quyền truy cập!')
        return redirect('/')
    if request.method == 'POST':
        if update_class_data(request.form):
            flash('Cập nhật lớp học thành công!')
        else:
            flash('Bạn không có quyền cập nhật lớp học cho học phần này!')
        return redirect('/classes')
    classes = get_classes_data()
    class_ = next((c for c in classes if c[0] == class_id), None)
    form_data = get_class_form_data()
    return render_template('classes_form.html', class_=class_, semesters=form_data['semesters'], courses=form_data['courses'])

@bp.route('/classes/delete/<int:class_id>')
@login_required
def classes_delete(class_id):
    if current_user.role not in ['admin', 'department_admin']:
        flash('Không có quyền truy cập!')
        return redirect('/')
    delete_class_data(class_id)
    flash('Xóa lớp học thành công!')
    return redirect('/classes')

@bp.route('/class_stats', methods=['GET', 'POST'])
@login_required
def class_stats():
    if current_user.role not in ['admin', 'department_admin']:
        flash('Không có quyền truy cập!')
        return redirect('/')
    academic_years = get_academic_years()
    stats = []
    if request.method == 'POST':
        stats = get_class_stats_data(request.form)
    return render_template('class_stats.html', stats=stats, academic_years=academic_years)

@bp.route('/class_assignments')
@login_required
def class_assignments():
    if current_user.role not in ['admin', 'department_admin']:
        flash('Không có quyền truy cập!')
        return redirect('/')
    teachers = get_teachers_data()
    assignments = {}
    for teacher in teachers:
        assignments[teacher[0]] = get_assigned_classes_data(teacher[0])
    return render_template('class_assignments.html', teachers=teachers, assignments=assignments)

@bp.route('/class_assignments/add', methods=['GET', 'POST'])
@login_required
def class_assignments_add():
    if current_user.role not in ['admin', 'department_admin']:
        flash('Không có quyền truy cập!')
        return redirect('/')
    if request.method == 'POST':
        if assign_class_data(request.form):
            flash('Phân công lớp học thành công!')
        else:
            flash('Bạn không có quyền phân công lớp học này!')
        return redirect('/class_assignments')
    teachers = get_teachers_data()
    unassigned_classes = get_unassigned_classes_data()
    return render_template('class_assignment_form.html', teachers=teachers, classes=unassigned_classes)

@bp.route('/class_assignments/remove', methods=['POST'])
@login_required
def class_assignments_remove():
    if current_user.role not in ['admin', 'department_admin']:
        flash('Không có quyền truy cập!')
        return redirect('/class_assignments')
    if 'remove_classes' in request.form:
        for class_teacher_id in request.form.getlist('remove_classes'):
            class_id, teacher_id = class_teacher_id.split('_')
            if remove_assignment_data({'teacher_id': teacher_id, 'class_id': class_id}):
                flash('Hủy phân công lớp học thành công!')
            else:
                flash('Bạn không có quyền hủy phân công lớp học này!')
    return redirect('/class_assignments')