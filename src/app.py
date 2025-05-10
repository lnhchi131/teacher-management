from flask import Flask
from models import db, User
from routes import register_routes
from dotenv import load_dotenv
import os

load_dotenv()  # Tải biến từ .env

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')

db.init_app(app)

with app.app_context():
    db.create_all()
    if not db.session.query(db.exists().where(User.username == 'admin')).scalar():
        from werkzeug.security import generate_password_hash
        admin = User(username='admin', password=generate_password_hash('admin123'))
        db.session.add(admin)
        db.session.commit()

register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
