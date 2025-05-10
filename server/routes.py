import logging
from datetime import datetime

import pandas as pd
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename

from models import db, User
from models.quiz import Quiz, Question, Answer, QuizResult, UploadQuizForm
from server.forms import QuizForm, QuestionForm

quiz_bp = Blueprint('quiz', __name__)

logging.basicConfig(level=logging.DEBUG)

ALLOWED_EXTENSIONS = {'xlsx', 'xls'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Главная страница
@quiz_bp.route('/')
@login_required
def index():
    search_query = request.args.get('search', '')  # Поиск по названию
    date_filter = request.args.get('date_filter', '')  # Поиск по дате

    # Фильтруем квизы по названию, если задан запрос
    quizzes_query = Quiz.query.filter(Quiz.title.contains(search_query))

    # Добавляем фильтрацию по дате, если задано
    if date_filter:
        if date_filter == 'asc':
            quizzes_query = quizzes_query.order_by(Quiz.created_at.asc())
        elif date_filter == 'desc':
            quizzes_query = quizzes_query.order_by(Quiz.created_at.desc())

    quizzes = quizzes_query.all()

    return render_template('quiz/index.html', quizzes=quizzes)


# Добавление нового квиза (только для администратора)
@quiz_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_quiz():
    if not current_user.is_admin:
        flash('Только администраторы могут добавлять тесты', 'warning')
        return redirect(url_for('quiz.index'))

    form = QuizForm()

    if request.method == 'POST' and 'add_question' in request.form:
        form.questions.append_entry()
        return render_template('quiz/add_quiz.html', form=form)

    if form.validate_on_submit():
        quiz = Quiz(title=form.title.data)
        db.session.add(quiz)
        db.session.flush()

        for qform in form.questions.entries:
            question_form = qform.form
            question = Question(text=question_form.text.data, quiz_id=quiz.id)
            db.session.add(question)
            db.session.flush()

            options = {
                'A': question_form.option_a.data,
                'B': question_form.option_b.data,
                'C': question_form.option_c.data,
                'D': question_form.option_d.data
            }

            for key, text in options.items():
                db.session.add(Answer(
                    question_id=question.id,
                    text=text,
                    is_correct=(key == question_form.correct_answer.data)
                ))

        db.session.commit()
        flash('Квиз успешно сохранён!', 'success')
        return redirect(url_for('quiz.view_questions'))

    if request.method == 'GET' and len(form.questions) == 0:
        form.questions.append_entry()

    return render_template('quiz/add_quiz.html', form=form)


# Страница для загрузки квиза из Excel файла
@quiz_bp.route('/upload_file', methods=['GET', 'POST'])
@login_required
def upload_quiz():
    form = UploadQuizForm()
    quiz_data = None

    if request.method == 'POST' and form.validate_on_submit():
        file = form.quiz_file.data
        filename = secure_filename(file.filename)

        try:
            df = pd.read_excel(file)
        except Exception:
            flash('Ошибка при чтении Excel-файла. Убедитесь, что файл корректный.', 'danger')
            return render_template('quiz/upload_quiz.html', form=form)

        required_columns = ['question', 'answer_a', 'answer_b', 'answer_c', 'answer_d', 'is_correct']
        if not all(col in df.columns for col in required_columns):
            flash('Файл должен содержать все столбцы: question, answer_a, answer_b, answer_c, answer_d, is_correct',
                  'danger')
            return render_template('quiz/upload_quiz.html', form=form)

        quiz_title = request.form.get('quiz_name', '').strip()
        if not quiz_title:
            flash('Введите название квиза.', 'warning')
            return render_template('quiz/upload_quiz.html', form=form)

        # Проверка на дубликаты по названию и вопросам
        existing_quiz = Quiz.query.filter_by(title=quiz_title).first()
        if existing_quiz:
            existing_questions = {q.text.strip().lower() for q in existing_quiz.questions}
            new_questions = {str(q).strip().lower() for q in df['question'].tolist()}
            if new_questions == existing_questions:
                flash('Такой квиз уже существует.', 'warning')
                return redirect(url_for('quiz.index'))

        # Сохраняем квиз в базу
        new_quiz = Quiz(title=quiz_title, created_at=datetime.utcnow())
        db.session.add(new_quiz)
        db.session.flush()  # Получаем quiz.id

        quiz_data = []

        for _, row in df.iterrows():
            question_text = str(row['question']).strip()
            correct_key = str(row['is_correct']).strip().upper()

            question = Question(text=question_text, quiz_id=new_quiz.id)
            db.session.add(question)
            db.session.flush()  # Получаем question.id

            for key in ['A', 'B', 'C', 'D']:
                answer_text = str(row[f'answer_{key.lower()}']).strip()
                is_correct = (key == correct_key)
                answer = Answer(text=answer_text, is_correct=is_correct, question_id=question.id)
                db.session.add(answer)

            quiz_data.append({
                'question': question_text,
                'answer_a': row['answer_a'],
                'answer_b': row['answer_b'],
                'answer_c': row['answer_c'],
                'answer_d': row['answer_d'],
                'is_correct': correct_key
            })

        db.session.commit()
        flash('Квиз успешно загружен и сохранён в базе.', 'success')

    return render_template('quiz/upload_quiz.html', form=form, quiz_data=quiz_data)


# Редактирование вопроса
@quiz_bp.route('/question/edit/<int:question_id>', methods=['GET', 'POST'])
@login_required
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    answers = Answer.query.filter_by(question_id=question.id).order_by(Answer.id).all()

    form = QuestionForm(obj=question)

    if len(answers) >= 4:
        answer_map = {
            'A': answers[0],
            'B': answers[1],
            'C': answers[2],
            'D': answers[3],
        }

        if request.method == 'GET':
            form.option_a.data = answer_map['A'].text
            form.option_b.data = answer_map['B'].text
            form.option_c.data = answer_map['C'].text
            form.option_d.data = answer_map['D'].text

            for key, ans in answer_map.items():
                if ans.is_correct:
                    form.correct_answer.data = key
                    break

        elif form.validate_on_submit():
            question.text = form.text.data
            db.session.add(question)

            answer_map['A'].text = form.option_a.data
            answer_map['B'].text = form.option_b.data
            answer_map['C'].text = form.option_c.data
            answer_map['D'].text = form.option_d.data

            correct_key = form.correct_answer.data
            for key, ans in answer_map.items():
                ans.is_correct = (key == correct_key)
                db.session.add(ans)

            db.session.commit()
            flash('Вопрос успешно обновлён!', 'success')
            return redirect(url_for('quiz.view_questions'))

    else:
        flash("Ошибка: У вопроса недостаточно вариантов ответа", "danger")
        return redirect(url_for('quiz.view_questions'))

    return render_template('quiz/edit_question.html', form=form, question=question)


# Страница с прохождением квиза
@quiz_bp.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)

    if request.method == 'POST':
        correct = 0
        total = len(quiz.questions)

        for question in quiz.questions:
            selected = request.form.get(str(question.id))
            if selected:
                answer = Answer.query.get(selected)
                if answer and answer.is_correct:
                    correct += 1

        percent = int((correct / total) * 100)
        result = QuizResult(user_id=current_user.id, quiz_id=quiz.id,
                            score=correct, total=total, percent=percent)
        db.session.add(result)
        db.session.commit()
        return redirect(url_for('quiz.result', result_id=result.id))

    return render_template('quiz/take_quiz.html', quiz=quiz)


# Просмотр результата
@quiz_bp.route('/result/<int:result_id>')
@login_required
def result(result_id):
    result = QuizResult.query.get_or_404(result_id)
    return render_template('quiz/result.html', result=result)


# Просмотр всех вопросов (только для администратора)
@quiz_bp.route('/questions', methods=['GET', 'POST'])
@login_required
def view_questions():
    search_query = request.args.get('search', '').strip()

    if search_query:
        questions = Question.query.filter(Question.quiz.has(Quiz.title.like(f'%{search_query}%'))).all()
    else:
        questions = Question.query.all()

    for question in questions:
        all_answers = Answer.query.filter_by(question_id=question.id).all()
        correct_answers = [a for a in all_answers if a.is_correct]
        question.correct_answer = correct_answers[0].text if correct_answers else 'нет ответа'
        question.answers = all_answers

    return render_template('quiz/view_questions.html', questions=questions, search_query=search_query)


# История прохождений квизов (только для администратора)
@quiz_bp.route('/history')
@login_required
def quiz_history():
    if not current_user.is_admin:
        flash("История доступна только администраторам", "warning")
        return redirect(url_for('quiz.index'))

    results = QuizResult.query.options(
        joinedload(QuizResult.quiz),
        joinedload(QuizResult.user)
    ).order_by(QuizResult.timestamp.desc()).all()

    return render_template('quiz/history.html', results=results)


# Просмотр всех пользователей (только для администратора)
@quiz_bp.route('/users')
@login_required
def view_users():
    if not current_user.is_admin:
        flash("Доступ только для администраторов", "warning")
        return redirect(url_for('quiz.index'))

    users = User.query.all()
    return render_template('quiz/view_users.html', users=users)


# Удаление квиза (только для администратора)
@quiz_bp.route('/quiz/delete/<int:quiz_id>', methods=['POST'])
@login_required
def delete_quiz(quiz_id):
    if not current_user.is_admin:
        flash('Удаление разрешено только администраторам.', 'danger')
        return redirect(url_for('quiz.index'))

    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    flash(f'Квиз «{quiz.title}» удалён.', 'success')
    return redirect(url_for('quiz.index'))


# Удаление вопроса (только для администратора)
@quiz_bp.route('/question/delete/<int:question_id>', methods=['POST', 'GET'])
@login_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)

    if not current_user.is_admin:
        flash("Удаление разрешено только администраторам", "danger")
        return redirect(url_for('quiz.view_questions'))

    db.session.delete(question)
    db.session.commit()
    flash("Вопрос удалён", "success")
    return redirect(url_for('quiz.view_questions'))
