from celery import Celery
from datetime import datetime, timedelta
from flask import Flask, render_template_string
from models import db, User, BookIssuance
from mail import send_email  
import os

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config.from_pyfile('config.py')

celery = make_celery(app)

@app.cli.command("send_daily_reminders")
@celery.task
def send_daily_reminders():
    today = datetime.now().date()
    users = User.query.filter(User.last_login >= today).all()
    msg_body = f"Hi {user.name},\n\nPlease visit our app today to explore new features and updates.\n\nThank you!\n"
    sub = "Reminder: Visit Our App"
    for user in users:
        send_email(user.email, sub, msg_body)

@app.cli.command("generate_monthly_report")
@celery.task
def generate_monthly_report():
    today = datetime.now()
    current_month = today.month
    current_year = today.year
    
    first_day_of_month = datetime(current_year, current_month, 1)
    
    users = User.query.all()

    for user in users:
        issuances = BookIssuance.query.filter_by(user_id=user.id).filter(BookIssuance.issued_date >= first_day_of_month).all()

        html_content = render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Monthly Activity Report - {{ month }} {{ year }} - {{ user_name }}</title>
        </head>
        <body>
            <h1>Monthly Activity Report - {{ month }} {{ year }} - {{ user_name }}</h1>
            <h2>E-Books Issued by {{ user_name }}</h2>
            <table border="1">
                <thead>
                    <tr>
                        <th>Issued Date</th>
                        <th>Book</th>
                    </tr>
                </thead>
                <tbody>
                    {% for issuance in issuances %}
                    <tr>
                        <td>{{ issuance.issued_date }}</td>
                        <td>{{ issuance.book.title }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </body>
        </html>
        """, month=first_day_of_month.strftime('%B'), year=current_year, user_name=user.name, issuances=issuances)

        send_email(user.email,"Monthly Activity Report", html_content)