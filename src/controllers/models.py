# controllers/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum as SQLAlchemyEnum, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime # Cần thiết nếu bạn muốn các giá trị default là thời gian hiện tại

db = SQLAlchemy()

# 1. Bảng User (Ví dụ, bạn đã có trong routes.py)
class User(db.Model):
    __tablename__ = 'users' # Đặt tên bảng tường minh
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) # Nên lưu trữ hash password

    def __repr__(self):
        return f'<User {self.username}>'

# 2. Bảng Quản Lý Khoa (Faculty)
class Faculty(db.Model):
    __tablename__ = 'QuanLyKhoa'
    MaKhoa = db.Column(db.String(10), primary_key=True)
    TenKhoa = db.Column(db.String(255), nullable=False, unique=True)
    MaGVTruongKhoa = db.Column(db.String(10), db.ForeignKey('DanhSachGiaoVien.MaGV'), nullable=True)
    SoLuongBoMon = db.Column(db.Integer, default=0)
    SoLuongChuongTrinhDaoTao = db.Column(db.Integer, default=0)
    NgayThanhLap = db.Column(Date, nullable=True)
    TrangThai = db.Column(SQLAlchemyEnum('Hoạt động', 'Ngừng hoạt động', 'Tạm dừng', name='trang_thai_khoa_enum'), default='Hoạt động')

    # Mối quan hệ: Một khoa có nhiều giáo viên
    # `lazy='dynamic'` cho phép bạn thực hiện các truy vấn thêm (filter, order_by) trên tập hợp giáo viên
    teachers = db.relationship('Teacher', back_populates='faculty', foreign_keys='Teacher.MaKhoa', lazy='dynamic')

    # Mối quan hệ: Một khoa có một trưởng khoa (là một Teacher)
    # `uselist=False` vì đây là mối quan hệ một-một (hoặc một-không) từ phía Khoa
    head_teacher = db.relationship('Teacher', foreign_keys=[MaGVTruongKhoa], backref=db.backref('faculty_led_by', uselist=False))

    def __repr__(self):
        return f'<Faculty {self.TenKhoa}>'

# 3. Bảng Quản Lý Bằng Cấp (Degree)
class Degree(db.Model):
    __tablename__ = 'QuanLyBangCap'
    MaBangCap = db.Column(db.String(10), primary_key=True)
    TenBangCap = db.Column(db.String(255), nullable=False, unique=True)

    # Mối quan hệ: Một loại bằng cấp có thể được nhiều giáo viên sở hữu (thông qua TeacherDegree)
    teacher_degrees = db.relationship('TeacherDegree', back_populates='degree_info', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Degree {self.TenBangCap}>'

# 4. Bảng Danh Sách Giáo Viên (Teacher)
class Teacher(db.Model):
    __tablename__ = 'DanhSachGiaoVien'
    MaGV = db.Column(db.String(10), primary_key=True)
    HoTen = db.Column(db.String(255), nullable=False)
    MaKhoa = db.Column(db.String(10), db.ForeignKey('QuanLyKhoa.MaKhoa'), nullable=True)
    HeSo = db.Column(Numeric(5,2), nullable=False, default=1.00) # DECIMAL(5,2)

    # Mối quan hệ: Một giáo viên thuộc về một khoa
    faculty = db.relationship('Faculty', back_populates='teachers', foreign_keys=[MaKhoa])

    # Mối quan hệ: Một giáo viên có thể có nhiều bằng cấp (thông qua TeacherDegree)
    degrees_info = db.relationship('TeacherDegree', back_populates='teacher_info', cascade="all, delete-orphan")
    
    # Helper property để dễ dàng lấy danh sách các đối tượng Degree
    @property
    def degrees(self):
        return [td.degree_info for td in self.degrees_info]

    def __repr__(self):
        return f'<Teacher {self.HoTen}>'

# 5. Bảng liên kết GiaoVien_BangCap (TeacherDegree)
# Đây là model cho bảng trung gian vì nó có thêm các cột ngoài 2 khóa ngoại
class TeacherDegree(db.Model):
    __tablename__ = 'GiaoVien_BangCap'
    MaGV = db.Column(db.String(10), db.ForeignKey('DanhSachGiaoVien.MaGV'), primary_key=True)
    MaBangCap = db.Column(db.String(10), db.ForeignKey('QuanLyBangCap.MaBangCap'), primary_key=True)
    NgayCapBang = db.Column(Date, nullable=True)
    NoiCapBang = db.Column(db.String(255), nullable=True)

    # Mối quan hệ ngược lại với Teacher và Degree
    teacher_info = db.relationship('Teacher', back_populates='degrees_info')
    degree_info = db.relationship('Degree', back_populates='teacher_degrees')

    def __repr__(self):
        return f'<TeacherDegree GV: {self.MaGV} - BC: {self.MaBangCap}>'

# 6. Bảng Class (Lớp học) - Dựa trên import của bạn, có thể bạn cần nó
class Class(db.Model):
    __tablename__ = 'classes' # Hoặc tên bảng bạn muốn
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Thêm các trường khác cho lớp học nếu cần
    # Ví dụ: MaGVChuNhiem = db.Column(db.String(10), db.ForeignKey('DanhSachGiaoVien.MaGV'), nullable=True)
    # teacher_in_charge = db.relationship('Teacher', foreign_keys=[MaGVChuNhiem])
    
    def __repr__(self):
        return f'<Class {self.name}>'