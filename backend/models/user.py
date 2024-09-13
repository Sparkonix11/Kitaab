from models import db, BookIssuance
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    image = db.Column(db.String(200), nullable=False, default='/static/user_placeholder.png')
    last_login = db.Column(db.DateTime)

    # Define relationships with BookIssuance
    borrowed_books = db.relationship('BookIssuance', back_populates='user', overlaps="requested_books")
    requested_books = db.relationship('BookIssuance', back_populates='user', overlaps="borrowed_books")
    book_issuances = db.relationship('BookIssuance', back_populates='user', overlaps="borrowed_books,requested_books")
    feedbacks = db.relationship('Feedback', back_populates='user')




    @property
    def is_librarian(self):
        # Assume there is a 'role' field in the User model
        return self.role == 'librarian'

    def has_max_requested_books(self):
        return BookIssuance.query.filter_by(user_id=self.id, is_returned=False).count() >= 5

    def has_requested_book(self, book):
        for issuance in self.requested_books:
            if issuance.book == book and not issuance.is_returned:
                return True
        return False

    def has_max_borrowed_books(self):
        # Count the number of borrowed books that are not returned
        count = sum(1 for issuance in self.borrowed_books if not issuance.is_returned)
        return count >= 5

    def has_borrowed_book(self, book):
        # Check if the user has borrowed the specified book and it's not returned
        for issuance in self.borrowed_books:
            if issuance.book == book and not issuance.is_returned:
                return True
        return False

    def get_book_issuance(self, book):
        for issuance in self.book_issuances:
            if issuance.book == book:
                return issuance
        return None