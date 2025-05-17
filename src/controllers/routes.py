from flask import render_template, request, redirect, url_for, session, flash
from .models import *
from datetime import datetime
from werkzeug.security import check_password_hash

def register_routes(app):
    @app.route('/')
    def home():
        return redirect(url_for('trangchu'))

    # ========== Trang chủ ==========
    @app.route('/trangchu')
    def trangchu():
        return render_template('trangchu.html')

    # ========== Báo cáo tiền dạy ==========
    @app.route('/baocao/nam')
    def baocao_nam():
        return render_template('baocaotienday/trongmotnam.html')

    @app.route('/baocao/khoa')
    def baocao_khoa():
        return render_template('baocaotienday/trongmoykhoa.html')

    @app.route('/baocao/toantruong')
    def baocao_toantruong():
        return render_template('baocaotienday/toantruong.html')

    # ========== Quản lý giáo viên ==========
    @app.route('/giaovien')
    @app.route('/giaovien/<section>')
    @app.route('/giaovien/<section>/<action>')
    def quanly_giaovien(section='giaovien', action=None):
        template_map = {
            'giaovien': 'quanlygiaovien/quanlygiaovien.html',
            'bangcap': 'quanlygiaovien/quanlybangcap.html',
            'khoa': 'quanlygiaovien/quanlykhoa.html',
            'thongke': 'quanlygiaovien/thongkegiaovien.html'
        }
        if section == 'bangcap' and action == 'them':
            if request.method == 'POST':
                degree_type = request.form.get('degree_type')
                teacher_id = request.form.get('teacher_id')
                # Create new Degree record
                new_degree = Degree(
                    name=degree_type,
                    teacher_id=teacher_id
                )
                db.session.add(new_degree)
                db.session.commit()
                flash('Thêm bằng cấp thành công!', 'success')
                return redirect(url_for('quanly_giaovien', section='bangcap'))
            # GET request: render form
            teachers = Teacher.query.all()
            return render_template('quanlygiaovien/thembangcap.html', teachers=teachers)
        template = template_map.get(section, 'quanlygiaovien/quanlygiaovien.html')
        return render_template(template)

    # ========== Quản lý lớp học ==========
    @app.route('/lophoc/hocphan')
    def quanly_hocphan():
        return render_template('quanlylophoc/quanlyhocphan.html')

    @app.route('/lophoc/kihoc')
    def quanly_kihoc():
        return render_template('quanlylophoc/quanlykihoc.html')

    @app.route('/lophoc/thoikhoabieu')
    def quanly_tkb():
        return render_template('quanlylophoc/quanlythoikhoabieu.html')

    @app.route('/lophoc/thongke')
    def thongke_lophoc():
        return render_template('quanlylophoc/thongkelop.html')

    # ========== Tính tiền dạy ==========
    @app.route('/tienday/hesogiaovien')
    def heso_giaovien():
        return render_template('tinhtienday/hesogiaovien.html')

    @app.route('/tienday/hesolop')
    def heso_lop():
        return render_template('tinhtienday/hesolop.html')

    @app.route('/tienday/phancong')
    def phancong_giangvien():
        return render_template('tinhtienday/phanconggiangvien.html')

    @app.route('/tienday/sotienmottiet')
    def sotien_mottiet():
        return render_template('tinhtienday/sotienchomottiet.html')

    @app.route('/tienday')
    def tinhtienday():
        return render_template('tinhtienday/tinhtienday.html')