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
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255)
);

-- Bảng degrees: Liên kết giữa giáo viên và bằng cấp (lưu trực tiếp tên bằng cấp)
CREATE TABLE degrees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL CHECK (name IN ('Thạc sĩ', 'Tiến sĩ', 'Giáo sư', 'Phó giáo sư', 'Cử nhân')),
    teacher_id INT,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id),
    UNIQUE (teacher_id) -- Mỗi giáo viên chỉ có một bằng cấp
);

-- Bảng faculty: Lưu thông tin khoa
CREATE TABLE faculty (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    abbreviation VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255)
);

-- Bảng classes: Liên kết giữa giáo viên và khoa
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
INSERT INTO teachers (code, name, birth_date, phone, email) VALUES 
    ('GV001', 'Nguyễn Văn A', '1980-05-15', '0123456789', 'gv001@school.edu.vn'), 
    ('GV002', 'Trần Thị B', '1975-08-22', '0987654321', 'gv002@school.edu.vn'), 
    ('GV003', 'Lê Văn C', '1990-03-10', '0912345678', 'gv003@school.edu.vn');

-- Bằng cấp
INSERT INTO degrees (name, teacher_id) VALUES 
    ('Thạc sĩ', 1),  -- Thạc sĩ cho GV001
    ('Tiến sĩ', 2),  -- Tiến sĩ cho GV002
    ('Giáo sư', 3);  -- Giáo sư cho GV003

-- Khoa
INSERT INTO faculty (name, abbreviation, description) VALUES 
    ('Toán Cao cấp', 'TCC', 'Khoa Toán Cao cấp'), 
    ('Vật lý Đại cương', 'VLDC', 'Khoa Vật lý Đại cương'), 
    ('Hoá học Cơ bản', 'HLCB', 'Khoa Hoá học Cơ bản');

-- Lớp học
INSERT INTO classes (teacher_id, faculty_id) VALUES 
    (1, 1),  -- GV001 dạy Toán Cao cấp
    (1, 2),  -- GV001 dạy Vật lý Đại cương
    (2, 1),  -- GV002 dạy Toán Cao cấp
    (3, 3);  -- GV003 dạy Hoá học Cơ bản

-- Báo cáo
INSERT INTO reports (details) VALUES 
    ('Báo cáo tháng 5: Hoạt động giảng dạy ổn định.');