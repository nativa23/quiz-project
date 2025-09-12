from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FieldList, FormField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[
        DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class QuestionForm(FlaskForm):
    class Meta:
        csrf = False  # Отключаем CSRF только для вложенной формы

    text = StringField('Вопрос', validators=[DataRequired()])
    option_a = StringField('Вариант A', validators=[DataRequired()])
    option_b = StringField('Вариант B', validators=[DataRequired()])
    option_c = StringField('Вариант C', validators=[DataRequired()])
    option_d = StringField('Вариант D', validators=[DataRequired()])
    correct_answer = SelectField('Правильный ответ', choices=[
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')
    ], validators=[DataRequired()])


class QuizForm(FlaskForm):
    title = StringField('Название квиза', validators=[DataRequired()], name="quiz-title")
    questions = FieldList(FormField(QuestionForm), min_entries=1, max_entries=20)
    submit = SubmitField('Создать квиз')


class AnswerForm(FlaskForm):
    text = StringField('Ответ', validators=[DataRequired()])
    is_correct = SelectField('Правильный ответ', choices=[('yes', 'Да'), ('no', 'Нет')])


class QuestionForm(FlaskForm):
    text = StringField('Текст вопроса', validators=[DataRequired()])
    option_a = StringField('Вариант A', validators=[DataRequired()])
    option_b = StringField('Вариант B', validators=[DataRequired()])
    option_c = StringField('Вариант C', validators=[DataRequired()])
    option_d = StringField('Вариант D', validators=[DataRequired()])
    correct_answer = StringField('Правильный ответ', validators=[DataRequired()])
    submit = SubmitField('Сохранить изменения')
