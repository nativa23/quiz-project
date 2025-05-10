from werkzeug.security import generate_password_hash

from models import db
from models.user import User
from server.main import create_app

# Создание приложения и контекста
app = create_app()


def create_admin():
    email = input("Введите email администратора: ")
    password = input("Введите пароль администратора: ")

    # Проверка, существует ли пользователь с таким email
    if User.query.filter_by(email=email).first():
        print("Пользователь с таким email уже существует.")
        return

    hashed_password = generate_password_hash(password)
    admin = User(email=email, password=hashed_password, is_admin=True)

    db.session.add(admin)
    db.session.commit()
    print("Администратор создан успешно!")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Создание таблиц, если они ещё не существуют
        print("База данных и таблицы созданы")
        create_admin()
