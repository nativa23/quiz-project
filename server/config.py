import os

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


# Конфигурация Flask
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")  # для шифрования сессий
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL",
                                             f"sqlite:///{os.path.join(basedir, 'db.sqlite3')}")  # путь к БД
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # отключает уведомления

    # Параметры для загрузки файлов
    ALLOWED_EXTENSIONS = {'xlsx'}  # Разрешённые расширения для файлов
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Максимальный размер загружаемого файла (16MB)
