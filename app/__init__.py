import os

from flask import Flask
from dotenv import load_dotenv

from app.extensions import db, migrate, login_manager
from app.routes.main import main
from app.routes.professionals import professionals

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(professionals)

    return app