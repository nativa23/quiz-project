from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Импорт моделей после инициализации db
from models import user, quiz
from models.user import User
from models.quiz import Quiz, Question, Answer, QuizResult
