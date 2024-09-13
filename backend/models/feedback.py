from models import db
from datetime import datetime

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    feedback_type = db.Column(db.String(20), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Define relationships
    user = db.relationship('User', back_populates='feedbacks')
    book = db.relationship('Book', back_populates='feedbacks')

    def save(self):
        db.session.add(self)
        db.session.commit()