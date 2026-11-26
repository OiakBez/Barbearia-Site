import os

from flask import Flask
from dotenv import load_dotenv

from app.extensions import db, migrate, login_manager
from app.models import User, Professional, Service, Appointment
from app.routes.main import main
from app.routes.professionals import professionals
from app.routes.auth import auth

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except (ValueError, TypeError):
            return None

    app.register_blueprint(main)
    app.register_blueprint(professionals)
    app.register_blueprint(auth)

    return app