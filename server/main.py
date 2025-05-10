from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate  # Импортируем Flask-Migrate

from models import db
from server.auth import auth_bp
from server.config import Config
from server.routes import quiz_bp

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

from models.user import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Загружаем конфигурацию из config.py

    # Инициализация расширений
    db.init_app(app)

    # Инициализация миграций
    migrate = Migrate(app, db)

    # Логин-менеджер
    login_manager.init_app(app)

    # Регистрация Blueprint'ов
    app.register_blueprint(auth_bp)
    app.register_blueprint(quiz_bp)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
