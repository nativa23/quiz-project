import os
from flask import Flask
from server.config import Config
from models import db
from flask_login import LoginManager
from server.auth import auth_bp
from server.routes import quiz_bp
from flask_migrate import Migrate  # Импортируем Flask-Migrate

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

# Для запуска через `python main.py`
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
