from datetime import datetime

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from sqlalchemy.orm import relationship
from wtforms.fields.simple import SubmitField

from . import db


class Quiz(db.Model):
    __tablename__ = 'quizzes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Связь с вопросами
    questions = db.relationship('Question', back_populates='quiz', cascade='all, delete-orphan')

    # Связь с результатами тестов
    results = db.relationship('QuizResult', back_populates='quiz', cascade='all, delete-orphan')


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(512), nullable=False)  # Вопрос
    correct_answer = db.Column(db.String(512), nullable=True)  # Правильный ответ

    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    quiz = db.relationship('Quiz', back_populates='questions')

    # Связь с вариантами ответов
    answers = db.relationship('Answer', backref='question', lazy=True, cascade='all, delete-orphan')


class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(512), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)


class QuizResult(db.Model):
    __tablename__ = 'quiz_results'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    score = db.Column(db.Integer)
    total = db.Column(db.Integer)
    percent = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Связь с пользователем и квизом
    user = db.relationship('User', back_populates='results')
    quiz = db.relationship('Quiz', back_populates='results')


# Для загрузки квиза из Excel
class UploadQuizForm(FlaskForm):
    # Поле для загрузки файла
    quiz_file = FileField('Загрузите квиз (Excel файл)', validators=[
        FileRequired(),
        FileAllowed(['xlsx', 'xls'], 'Только файлы Excel разрешены')
    ])

    # Кнопка для отправки формы
    submit = SubmitField('Загрузить файл')
