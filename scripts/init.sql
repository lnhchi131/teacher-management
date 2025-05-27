CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(10) NOT NULL,
    name VARCHAR(255) NOT NULL,
    mission TEXT
);

CREATE TABLE degrees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    coefficient FLOAT NOT NULL
);

CREATE TABLE teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(10) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    dob DATE,
    phone VARCHAR(20),
    email VARCHAR(255),
    department_id INT,
    degree_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(id),
    FOREIGN KEY (degree_id) REFERENCES degrees(id)
);

CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(10) NOT NULL,
    name VARCHAR(255) NOT NULL,
    coefficient FLOAT NOT NULL,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE semesters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(10) NOT NULL,
    academic_year VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

CREATE TABLE classes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) NOT NULL,
    course_id INT,
    semester_id INT,
    hours INT NOT NULL,
    student_count INT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (semester_id) REFERENCES semesters(id)
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'department_admin', 'teacher') NOT NULL,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);