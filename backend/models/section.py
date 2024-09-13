from models import db

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    description = db.Column(db.Text)

    # Define a relationship with books
    books = db.relationship('Book', backref='section', lazy=True)