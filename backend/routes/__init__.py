from flask import Blueprint

from .main import main
from .auth import auth_api_bp
from .librarian import book_issue_return_api_bp, librarian_api_bp
from .general_user import general_user
from .section import section_api_bp
from .ebook import book_api_bp

def init_app(app):
    app.register_blueprint(main)
    app.register_blueprint(auth_api_bp, url_prefix='/auth')
    app.register_blueprint(book_issue_return_api_bp, url_prefix='/issue')
    app.register_blueprint(librarian_api_bp, url_prefix='/librarian')
    app.register_blueprint(general_user, url_prefix='/user')
    app.register_blueprint(section_api_bp, url_prefix='/section')
    app.register_blueprint(book_api_bp, url_prefix='/book')