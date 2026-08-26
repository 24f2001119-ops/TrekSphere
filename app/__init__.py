from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth.routes import auth_bp
    from .admin.routes import admin_bp
    from .staff.routes import staff_bp
    from .user.routes import user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(user_bp)

    with app.app_context():
        db.create_all()

        
        if not User.query.filter_by(email="admin@trek.com").first():
            from werkzeug.security import generate_password_hash

            admin = User(
                name="Administrator",
                email="admin@trek.com",
                password=generate_password_hash("admin123"),
                role="admin",
                approved=True,
                blacklisted=False
            )

            db.session.add(admin)
            db.session.commit()

    return app