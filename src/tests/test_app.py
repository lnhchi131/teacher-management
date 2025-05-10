import unittest
import os
import csv
from app import app, db
from models import User, Degree, Faculty, Teacher

class TestApp(unittest.TestCase):
    def setUp(self):
        # Cấu hình ứng dụng để test
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Xóa database sau mỗi test
        with app.app_context():
            db.session.remove()
            db.drop_all()
        if os.path.exists('test.db'):
            os.remove('test.db')

    def test_login_success(self):
        # Tạo user để test
        with app.app_context():
            user = User(username='testuser', password='testpass')
            db.session.add(user)
            db.session.commit()

        # Test đăng nhập thành công
        response = self.app.post('/login', data={
            'username': 'testuser',
            'password': 'testpass'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'QUẢN LÝ GIÁO VIÊN', response.data)

    def test_login_failure(self):
        # Test đăng nhập thất bại
        response = self.app.post('/login', data={
            'username': 'wronguser',
            'password': 'wrongpass'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Tên đăng nhập hoặc mật khẩu không đúng', response.data)

    def test_add_faculty(self):
        # Đăng nhập trước
        with app.app_context():
            user = User(username='testuser', password='testpass')
            db.session.add(user)
            db.session.commit()
        self.app.post('/login', data={'username': 'testuser', 'password': 'testpass'})

        # Test thêm khoa
        response = self.app.post('/faculty', data={
            'name': 'Công nghệ Thông tin',
            'abbreviation': 'CNTT',
            'description': 'Đặc thù kỹ sư CNTT'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Công nghệ Thông tin', response.data)

    def test_add_teacher(self):
        # Đăng nhập trước
        with app.app_context():
            user = User(username='testuser', password='testpass')
            degree = Degree(name='Thạc sĩ')
            faculty = Faculty(name='Công nghệ Thông tin', abbreviation='CNTT')
            db.session.add_all([user, degree, faculty])
            db.session.commit()
        self.app.post('/login', data={'username': 'testuser', 'password': 'testpass'})

        # Test thêm giáo viên
        response = self.app.post('/teacher', data={
            'code': 'GV001',
            'full_name': 'Nguyễn Văn A',
            'birth_date': '1980-01-01',
            'phone': '0901234567',
            'email': 'nva@example.com',
            'faculty_id': 1,
            'degree_id': 1
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nguyễn Văn A', response.data)

    def test_stats(self):
        # Đăng nhập trước
        with app.app_context():
            user = User(username='testuser', password='testpass')
            degree = Degree(name='Thạc sĩ')
            faculty = Faculty(name='Công nghệ Thông tin', abbreviation='CNTT')
            teacher = Teacher(code='GV001', full_name='Nguyễn Văn A', birth_date='1980-01-01', phone='0901234567', email='nva@example.com', faculty_id=1, degree_id=1)
            db.session.add_all([user, degree, faculty, teacher])
            db.session.commit()
        self.app.post('/login', data={'username': 'testuser', 'password': 'testpass'})

        # Test xem thống kê
        response = self.app.get('/stats', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Công nghệ Thông tin', response.data)
        self.assertIn(b'Thạc sĩ', response.data)

    def run_tests_and_save_to_csv(self):
        # Chạy tất cả test và lưu kết quả vào CSV
        test_results = []
        suite = unittest.TestLoader().loadTestsFromTestCase(TestApp)
        runner = unittest.TextTestRunner()
        result = runner.run(suite)

        # Thu thập kết quả
        for test, error in result.failures + result.errors:
            test_results.append({
                'Test Case': str(test),
                'Result': 'Fail',
                'Error': str(error)
            })
        for test in result.testsRun - len(result.failures) - len(result.errors):
            test_results.append({
                'Test Case': 'Test Passed',
                'Result': 'Pass',
                'Error': ''
            })

        # Lưu vào file CSV
        with open('test_results.csv', 'w', newline='') as csvfile:
            fieldnames = ['Test Case', 'Result', 'Error']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for result in test_results:
                writer.writerow(result)

if __name__ == '__main__':
    # Chạy test và lưu kết quả vào CSV
    test_suite = TestApp('run_tests_and_save_to_csv')
    test_suite.setUp()
    test_suite.run_tests_and_save_to_csv()
    test_suite.tearDown()