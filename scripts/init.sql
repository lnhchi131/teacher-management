-- Xóa cơ sở dữ liệu nếu đã tồn tại
DROP DATABASE IF EXISTS teacher_management;

-- Tạo cơ sở dữ liệu mới
CREATE DATABASE teacher_management;
USE teacher_management;

-- Bảng users: Lưu thông tin người dùng để đăng nhập
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Bảng teachers: Lưu thông tin giáo viên
CREATE TABLE teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL
);

-- Bảng degrees: Lưu thông tin bằng cấp của giáo viên
CREATE TABLE degrees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL CHECK (name IN ('Thạc sĩ', 'Tiến sĩ', 'Giáo sư', 'Phó giáo sư', 'Cử nhân')),
    teacher_id INT,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id),
    UNIQUE (teacher_id) -- Mỗi giáo viên chỉ có một bằng cấp
);

-- Bảng faculty: Lưu thông tin khoá học
CREATE TABLE faculty (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    abbreviation VARCHAR(225) NOT NULL UNIQUE,
    description VARCHAR(225)
);

-- Bảng classes: Lưu thông tin lớp học (liên kết giữa giáo viên và khoa)
CREATE TABLE classes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    teacher_id INT,
    faculty_id INT,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id),
    FOREIGN KEY (faculty_id) REFERENCES faculty(id)
);

-- Bảng reports: Lưu thông tin báo cáo
CREATE TABLE reports (
    id INT AUTO_INCREMENT PRIMARY KEY,
    details TEXT NOT NULL
);

-- Thêm dữ liệu mẫu
-- Người dùng đăng nhập
INSERT INTO users (username, password) VALUES ('admin', 'admin123');

-- Giáo viên
INSERT INTO teachers (name, birth_date) VALUES 
    ('Nguyễn Văn A', '1980-05-15'), 
    ('Trần Thị B', '1975-08-22'), 
    ('Lê Văn C', '1990-03-10');

-- Bằng cấp
INSERT INTO degrees (name, teacher_id) VALUES 
    ('Thạc sĩ', 1), 
    ('Tiến sĩ', 2), 
    ('Giáo sư', 3);

-- Khoá học
INSERT INTO faculty (name) VALUES 
    ('Toán Cao cấp'), 
    ('Vật lý Đại cương'), 
    ('Hoá học Cơ bản');

-- Lớp học
INSERT INTO classes (teacher_id, faculty_id) VALUES 
    (1, 1), 
    (1, 2), 
    (2, 1), 
    (3, 3);

-- Báo cáo
INSERT INTO reports (details) VALUES 
    ('Báo cáo tháng 5: Hoạt động giảng dạy ổn định.');

def add_faculty(self, name, abbreviation, description):
    self.model.add_faculty(name, abbreviation, description)