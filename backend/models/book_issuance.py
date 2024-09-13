from models import db
from datetime import datetime, timedelta

class BookIssuance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_issued = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    date_read = db.Column(db.DateTime)
    is_returned = db.Column(db.Boolean, default=False)

    # Define relationships with User and Book
    user = db.relationship('User', backref='book_issuance_records')
    book = db.relationship('Book', back_populates='issuances')