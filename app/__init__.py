from flask import Flask
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your-secret-key'
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'routes.login'

    @login_manager.user_loader
    def load_user(user_id):
        from .models.users_model import get_user_by_id
        return get_user_by_id(user_id)

    with app.app_context():
        from .routes import routes, degree_routes, faculty_routes, teacher_routes, class_routes, teaching_payment_routes, class_coefficients_routes, teacher_coeff_routes, teaching_salary_routes, teaching_report_routes
        app.register_blueprint(routes.bp)
        app.register_blueprint(degree_routes.bp)
        app.register_blueprint(faculty_routes.bp)
        app.register_blueprint(teacher_routes.bp)
        app.register_blueprint(class_routes.bp)
        app.register_blueprint(teaching_payment_routes.bp)
        app.register_blueprint(class_coefficients_routes.bp)
        app.register_blueprint(teacher_coeff_routes.bp)  
        app.register_blueprint(teaching_salary_routes.bp)
        app.register_blueprint(teaching_report_routes.bp)
    return app