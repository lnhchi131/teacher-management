from flask import Flask
from flask_login import LoginManager
from flask_caching import Cache
from app.models.model import Model, User
import os

# Cấu hình caching
cache_config = {
    "CACHE_TYPE": "SimpleCache",  # Sử dụng bộ nhớ để lưu cache (phù hợp cho môi trường cục bộ)
    "CACHE_DEFAULT_TIMEOUT": 300  # Cache 5 phút
}

# Khởi tạo ứng dụng Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()
app.config.from_mapping(cache_config)

# Khởi tạo Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'

# Khởi tạo Flask-Caching
cache = Cache()
cache.init_app(app)

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

# Hàm tạo ứng dụng
def create_app():
    return app