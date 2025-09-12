# 🧠 Quiz Project

A web application built with Flask for creating, taking, and managing quizzes. It supports user registration, quiz
uploads from Excel files, and displaying results.

## 📌 Key Features

- User registration and login
- Roles: regular user and administrator
- Creating and editing quizzes
- Taking quizzes with result feedback
- Quiz history for users
- Uploading quizzes from Excel files
- Viewing users and quiz questions (admin-only)

## 🚀 Installation and Launch

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/quiz_project.git
cd quiz_project
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the database

```bash
python server/init_db.py
```

### 5. Run the application

```bash
python server/main.py
```

The app will be available at: http://localhost:5000

## 🗃️ Project Structure

```
quiz_project/
├── README.md # Project description
├── requirements.txt # Dependencies
├── db.sqlite3 # SQLite database file
├── static/
│ └── style.css # Application styles
├── models/
│ ├── init.py
│ ├── quiz.py # Quiz and question models
│ └── user.py # User model
├── server/
│ ├── init.py
│ ├── main.py # App entry point
│ ├── config.py # Flask configuration
│ ├── routes.py # Core routes
│ ├── auth.py # Authentication and registration
│ ├── forms.py # Flask-WTF forms
│ ├── init_db.py # DB initialization script
│ ├── migrations/ # Database migrations
│ └── templates/
│ ├── base.html
│ ├── auth/
│ │ ├── login.html
│ │ └── register.html
│ ├── quiz/
│ │ ├── index.html
│ │ ├── add_quiz.html
│ │ ├── upload_quiz.html
│ │ ├── take_quiz.html
│ │ ├── result.html
│ │ ├── history.html
│ │ ├── view_questions.html
│ │ ├── view_users.html
│ │ └── edit_question.html
│ └── macros/
│ └── question_form.html
```

## 🧪 Sample Quizzes

You can try out the quiz upload feature using sample files provided in the [`sample_quizzes/`](./sample_quizzes)
directory.

Each file is a ready-to-use Excel quiz. To test:

1. Open the web app.
2. Go to the "Upload Quiz" page.
3. Choose one of the `.xlsx` files from `sample_quizzes/`.
4. Click upload and start the quiz!

> Column headers required in the Excel file:
> `question`, `answer_a`, `answer_b`, `answer_c`, `answer_d`, `is_correct`

## 🧰 Tech Stack

- [Python 3](https://www.python.org/) — primary programming language
- [Flask](https://flask.palletsprojects.com/) — lightweight web framework
- [Flask-WTF](https://flask-wtf.readthedocs.io/) — form handling and validation
- [Flask-Login](https://flask-login.readthedocs.io/) — user session management
- [Flask-Migrate](https://flask-migrate.readthedocs.io/) + [Alembic](https://alembic.sqlalchemy.org/) — database
  migrations
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM for database interaction
- [SQLite](https://www.sqlite.org/index.html) — lightweight embedded database
- [Pandas](https://pandas.pydata.org/) — Excel file parsing and data handling
- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML) + [Jinja2](https://jinja.palletsprojects.com/) — template
  engine for dynamic HTML rendering
- [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) — styling for the user interface

## 📄 License

This project is completely open and unrestricted. No license applies — you are free to use, modify, and distribute it
without limitations.
