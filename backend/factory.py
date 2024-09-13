from flask import Flask
from models import db, init_db, User
from flask_login import LoginManager
from flask_cors import CORS
from flask_mail import Mail
from flask_caching import Cache
from routes import init_app
import os

login_manager = LoginManager()
mail = Mail()
cache = Cache()

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    app.config.from_pyfile('config.py')

    static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend/src/assets/static')
    book_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend/src/assets/static/books')
    book_cover_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend/src/assets/static/book_covers')

    app.config['UPLOAD_FOLDER'] = static_folder 
    app.config['UPLOAD_FOLDER_BOOK'] = book_folder
    app.config['UPLOAD_FOLDER_BOOK_COVER'] = book_cover_folder

    db.init_app(app)
    init_db(app)
    mail.init_app(app)
    login_manager.init_app(app)
    cache.init_app(app)

    app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379/1',
        CELERY_RESULT_BACKEND='redis://localhost:6379/2',
        CELERY_TIMEZONE='Asia/Kolkata',
        CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=True
    )

    from celery_tasks import celery
    celery.conf.update(app.config)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)

    init_app(app)

    return app
