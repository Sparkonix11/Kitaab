from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .book import Book
from .book_issuance import BookIssuance
from .request import Request
from .section import Section
from .user import User
from .feedback import Feedback

def init_db(app):
    with app.app_context():
        db.create_all()