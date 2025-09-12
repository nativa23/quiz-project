from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from models import db
from models.user import User
from server.forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Проверяем, существует ли пользователь с таким email
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Пользователь с таким email уже существует.', 'danger')
            return redirect(url_for('auth.register'))

        # Хешируем пароль перед сохранением
        hashed_password = generate_password_hash(form.password.data)

        # Создаем нового пользователя
        new_user = User(email=form.email.data, password=hashed_password, is_admin=False)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация прошла успешно. Войдите в аккаунт.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Находим пользователя по email
        user = User.query.filter_by(email=form.email.data).first()

        # Проверка на существующего пользователя и корректность пароля
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Вы успешно вошли.', 'success')
            return redirect(url_for('quiz.index'))

        flash('Неверный email или пароль.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта.', 'info')
    return redirect(url_for('auth.login'))
