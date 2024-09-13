from models import db

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_issuance_id = db.Column(db.Integer, db.ForeignKey('book_issuance.id'), nullable=False)
    request_date = db.Column(db.DateTime, default=db.func.current_timestamp())
