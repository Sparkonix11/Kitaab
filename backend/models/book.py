from models import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    author = db.Column(db.String(100))
    file_path = db.Column(db.String(200))
    book_cover = db.Column(db.String(200), default='/static/book_placeholder.png')

    # Define a foreign key relationship with sections
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))

    issuances = db.relationship('BookIssuance', back_populates='book', lazy='dynamic')
    feedbacks = db.relationship('Feedback', back_populates='book')