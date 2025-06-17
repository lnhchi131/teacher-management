INSERT INTO departments (code, name, mission) 
VALUES ('CNTT', 'Công nghệ Thông tin', 'Đào tạo kỹ sư CNTT'), 
       ('KHTN', 'Khoa học Tự nhiên', 'Nghiên cứu khoa học cơ bản');

INSERT INTO degrees (name, coefficient) 
VALUES ('Đại học', 1.3), 
       ('Thạc sĩ', 1.5), 
       ('Tiến sĩ', 1.7), 
       ('Phó giáo sư', 2.0), 
       ('Giáo sư', 2.5);

INSERT INTO teachers (code, full_name, dob, phone, email, department_id, degree_id) 
VALUES ('GV001', 'Nguyễn Thị A', '1980-05-15', '0123456789', 'nva@example.com', 1, 1),
       ('GV002', 'Trần Văn B', '1975-03-22', '0987654321', 'tvb@example.com', 2, 2);

INSERT INTO courses (code, name, coefficient, department_id) 
VALUES ('CS101', 'Lập trình cơ bản', 1.0, 1), 
       ('CS102', 'Cấu trúc dữ liệu', 1.0, 1), 
       ('MATH101', 'Toán cơ bản', 1.0, 2);

INSERT INTO semesters (code, academic_year, start_date, end_date) 
VALUES ('HK1', '2024-2025', '2024-09-01', '2025-01-15'),
       ('HK2', '2024-2025', '2025-02-01', '2025-06-15');

INSERT INTO classes (code, course_id, semester_id, hours, student_count) 
VALUES ('CS101-01', 1, 1, 45, 40),
       ('CS102-01', 2, 1, 45, 35),
       ('MATH101-01', 3, 1, 45, 35);

INSERT INTO teacher_class_assignments (teacher_id, class_id) 
VALUES (1, 1),  -- GV001 dạy CS101-01
       (1, 2),  -- GV001 dạy CS102-01 (thêm để kiểm tra nhiều lớp)
       (2, 3);  -- GV002 dạy MATH101-01

INSERT INTO users (username, password, role, department_id) 
VALUES ('admin', 'admin123', 'admin', NULL),
       ('dept_admin_cntt', 'dept123', 'department_admin', 1),
       ('dept_admin_khtn', 'dept123', 'department_admin', 2),
       ('GV001', 'gv001123', 'teacher', 1),
       ('GV002', 'gv002123', 'teacher', 2);

INSERT INTO teaching_rate (id, amount)
VALUES (1, 100000);

INSERT INTO class_coefficients (min_students, max_students, coefficient) VALUES
(0, 19, -0.3),
(20, 29, -0.2),
(30, 39, -0.1),
(40, 49, 0),
(50, 59, 0.1),
(60, 69, 0.2),
(70, 79, 0.3);