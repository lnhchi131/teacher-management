from flask import Flask
from flask_login import LoginManager
from app.models.model import Model, User
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24).hex()  # Tạo SECRET_KEY ngẫu nhiên

    # Khởi tạo Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # Load user từ ID
    @login_manager.user_loader
    def load_user(user_id):
        model = Model()
        cursor = model.connection.cursor()
        cursor.execute("SELECT id, username FROM users WHERE id = %s", (int(user_id),))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data:
            return User(user_data[0], user_data[1])
        return None

    # Đăng ký các route
    from app import routes
    app.register_blueprint(routes.bp)
    
    return app