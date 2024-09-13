# Import necessary modules
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from models import db, Book, BookIssuance, User, Section
import os
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# Create a Blueprint for book-related APIs
book_issue_return_api_bp = Blueprint('book_issue_return_api', __name__)
librarian_api_bp = Blueprint('librarian_api_bp', __name__)

# API for a user to request a book
@book_issue_return_api_bp.route('/books/request/<int:book_id>', methods=['POST'])
@login_required
def request_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    # Check if the user has already requested the maximum allowed books
    if current_user.has_max_requested_books():
        return jsonify({'message': 'Maximum requested books reached'}), 400

    # Check if the user has already requested this book
    if current_user.has_requested_book(book):
        # Check if the user has returned the book previously
        issuance = current_user.get_book_issuance(book)
        if issuance and issuance.is_returned:
            # If the book was returned previously, allow the user to request it again
            issuance.date_issued = None
            issuance.return_date = None
            db.session.commit()
            return jsonify({'message': 'Book requested successfully'}), 201
        else:
            return jsonify({'message': 'Book already requested'}), 400

    # Create a new book issuance record for the request
    issuance = BookIssuance(
        user=current_user,
        book=book
    )

    db.session.add(issuance)
    db.session.commit()

    return jsonify({'message': 'Book requested successfully'}), 201

# API for a user to read a book (access granted)
@book_issue_return_api_bp.route('/books/read/<int:book_id>', methods=['POST'])
@login_required
def read_book(book_id):
    book = Book.query.get(book_id)
    user = User.query.get(current_user.id)

    if not book:
        return jsonify({'message': 'Book not found'}), 404

    # Check if the user has requested this book and it's not yet returned
    issuance = BookIssuance.query.filter_by(book=book, user=user).order_by(BookIssuance.id.desc()).first()
    if not issuance or issuance.is_returned:
        return jsonify({'message': 'Book not requested or already returned'}), 400

    # Check if the book is read-accessible (date_issued is not None)
    if not issuance.date_issued:
        return jsonify({'message': 'Access not granted yet. Please wait for librarian approval.'}), 403

    # Check if the return date has passed
    if issuance.return_date and issuance.return_date < datetime.utcnow():
        # If return date has passed, mark the book as returned
        issuance.is_returned = True
        db.session.commit()
        return jsonify({'message': 'Book marked as returned because return date has passed.'}), 400

    # Update the issuance to mark the book as read
    issuance.date_read = datetime.utcnow()
    db.session.commit()

    return jsonify({'message': 'Access granted. Enjoy reading!'}), 200

# API for a librarian to issue a book to a user
@librarian_api_bp.route('/books/issue/<int:book_id>/<int:user_id>', methods=['POST'])
@login_required
def issue_book(book_id, user_id):
    # Check if the authenticated user is a librarian
    if not current_user.is_librarian:
        return jsonify({'message': 'Unauthorized. Librarian role required.'}), 403

    book = Book.query.get(book_id)
    user = User.query.get(user_id)

    if not book or not user:
        return jsonify({'message': 'Book or user not found'}), 404

    # Get the latest issuance record for the specified book and user
    existing_issuance = BookIssuance.query.filter_by(book=book, user=user).order_by(BookIssuance.id.desc()).first()
    
    if not existing_issuance or existing_issuance.is_returned:
        return jsonify({'message': 'User has not requested this book or already returned'}), 400

    # Check if the user has already borrowed this book
    if existing_issuance.date_issued is not None:
        return jsonify({'message': 'User already borrowed this book'}), 400

    # Update the existing issuance record with date issued and return date
    existing_issuance.date_issued = datetime.utcnow()
    existing_issuance.return_date = datetime.utcnow() + timedelta(days=7)
    db.session.commit()

    return jsonify({'message': 'Book issued successfully'}), 200


@book_issue_return_api_bp.route('/books/return/<int:book_id>', methods=['POST'])
@login_required
def return_book(book_id):
    # Get the book object from the database
    book = Book.query.get(book_id)
    
    # Check if the book exists
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    # Get the book issuance record for the current user
    issuance = BookIssuance.query.filter_by(book=book, user=current_user).order_by(BookIssuance.id.desc()).first()
    
    # Check if the user has issued this book
    if not issuance or issuance.is_returned:
        return jsonify({'message': 'Book not issued or already returned'}), 400
    
    # Update the issuance record to mark the book as returned
    issuance.is_returned = True
    db.session.commit()
    
    return jsonify({'message': 'Book returned successfully'}), 200


# API for a librarian to revoke access to a book from a user
@librarian_api_bp.route('/books/revoke/<int:book_id>/<int:user_id>', methods=['POST'])
@login_required
def revoke_access(book_id, user_id):
    # Check if the authenticated user is a librarian
    if not current_user.is_librarian:
        return jsonify({'message': 'Unauthorized. Librarian role required.'}), 403

    book = Book.query.get(book_id)
    user = User.query.get(user_id)

    if not book or not user:
        return jsonify({'message': 'Book or user not found'}), 404

    # Check if the user has borrowed this book
    issuance = BookIssuance.query.filter_by(book=book, user=user).order_by(BookIssuance.id.desc()).first()
    if not issuance or issuance.is_returned:
        return jsonify({'message': 'User has not borrowed this book or already returned'}), 400

    # Update the issuance to revoke access
    issuance.return_date = datetime.utcnow()
    db.session.commit()

    return jsonify({'message': 'Access revoked successfully'}), 200

@librarian_api_bp.route('/books/requests/pending', methods=['GET'])
@login_required
def get_pending_requests():
    # Check if the authenticated user is a librarian
    if not current_user.is_librarian:
        return jsonify({'message': 'Unauthorized. Librarian role required.'}), 403

    # Get all pending book issuance requests
    pending_requests = BookIssuance.query.filter_by(date_issued=None).all()

    # Prepare the response data
    pending_requests_data = [{
        'id': issuance.id,
        'book_id': issuance.book_id,
        'book_title': issuance.book.title,
        'user_id': issuance.user_id,
        'user_name': issuance.user.name,
        'user_email': issuance.user.email
    } for issuance in pending_requests]

    return jsonify(pending_requests_data), 200

@librarian_api_bp.route('/books/deny/<int:book_id>/<int:user_id>', methods=['POST'])
@login_required
def deny_request(book_id, user_id):
    # Check if the authenticated user is a librarian
    if not current_user.is_librarian:
        return jsonify({'message': 'Unauthorized. Librarian role required.'}), 403

    # Retrieve the book and user objects from the database
    book = Book.query.get(book_id)
    user = User.query.get(user_id)

    if not book or not user:
        return jsonify({'message': 'Book or user not found'}), 404

    # Find the book issuance record for the given book and user
    issuance = BookIssuance.query.filter_by(book=book, user=user, date_issued=None).first()

    if not issuance:
        return jsonify({'message': 'No pending request found for this book and user'}), 404

    # Delete the issuance record to deny the request
    db.session.delete(issuance)
    db.session.commit()

    return jsonify({'message': 'Request denied successfully'}), 200

@book_issue_return_api_bp.route('/books/approved', methods=['GET'])
@login_required
def get_approved_books():
    # Get all book issuance records where the book has been issued (date_issued is not null)
    approved_books = BookIssuance.query \
        .join(User, BookIssuance.user_id == User.id) \
        .filter(User.id == current_user.id, BookIssuance.date_issued.isnot(None)) \
        .all()

    # Filter out books that are already returned or not accessible for reading
    approved_books = [issuance for issuance in approved_books if not issuance.is_returned and issuance.date_issued]

    # Prepare the response data
    approved_books_data = [{
        'id': issuance.id,
        'book_id': issuance.book_id,
        'book_title': issuance.book.title,
        'book_file_path': issuance.book.file_path,
        'user_id': issuance.user_id,
        'user_name': issuance.user.name,
        'user_email': issuance.user.email,
        'date_issued': issuance.date_issued.strftime('%d-%m-%Y'),
        'return_date': issuance.return_date.strftime('%d-%m-%Y') if issuance.return_date else None
    } for issuance in approved_books]

    return jsonify(approved_books_data), 200

@librarian_api_bp.route('/books/approved', methods=['GET'])
@login_required
def get_approved_books():
    # Check if the authenticated user is a librarian
    if not current_user.is_librarian:
        return jsonify({'message': 'Unauthorized. Librarian role required.'}), 403

    # Get all book issuance records where the book has been issued (date_issued is not null) and is not returned
    approved_books = BookIssuance.query.filter(BookIssuance.date_issued.isnot(None), BookIssuance.is_returned.is_(False)).all()

    # Prepare the response data
    approved_books_data = [{
        'book_id': issuance.book_id,
        'book_title': issuance.book.title,
        'user_id': issuance.user_id,
        'user_name': issuance.user.name,
        'user_email': issuance.user.email,
        'date_issued': issuance.date_issued.strftime('%Y-%m-%d %H:%M:%S'),
        'return_date': issuance.return_date.strftime('%Y-%m-%d %H:%M:%S') if issuance.return_date else None
    } for issuance in approved_books]

    return jsonify(approved_books_data), 200


@librarian_api_bp.route('/dashboard_data', methods=['GET'])
@login_required
def librarian_dashboard():
    # Check if the authenticated user is a librarian
    if not current_user.is_librarian:
        return jsonify({'message': 'Unauthorized. Librarian role required.'}), 403

    # Get statistics for the librarian dashboard
    total_issued_books = BookIssuance.query.filter_by(is_returned=False).count()
    total_sections = Section.query.count()
    total_books = Book.query.count()

    # Get popular sections (sections with the most issued books)
    popular_sections = Section.query \
        .join(Book, Section.books) \
        .join(BookIssuance, Book.issuances) \
        .filter(BookIssuance.is_returned == False) \
        .group_by(Section.id) \
        .order_by(db.func.count(BookIssuance.id).desc()) \
        .limit(5) \
        .all()

    # Create a bar chart showing the number of issued books per section
    section_labels = [section.name for section in popular_sections]
    section_book_counts = [db.session.query(BookIssuance) \
                           .join(Book, BookIssuance.book) \
                           .join(Section, Book.section_id == Section.id) \
                           .filter(BookIssuance.is_returned == False, Section.id == section.id) \
                           .count() for section in popular_sections]

    plt.bar(section_labels, section_book_counts)
    plt.xlabel('Section')
    plt.ylabel('Number of Issued Books')
    plt.title('Number of Issued Books per Section')

    # Save the chart image to the static/charts folder
    chart_filename_1 = f'BooksperSections.png'
    charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../frontend/src/assets/static/charts')
    os.makedirs(charts_dir, exist_ok=True)  # Create the 'charts' directory if it doesn't exist
    chart_path = os.path.join(charts_dir, chart_filename_1)
    plt.savefig(chart_path, format='png')
    plt.close()

    # Now, let's integrate the logic of plot_books_borrowed_over_time() here

    # Query the database to get issuance dates
    issuances = BookIssuance.query.filter(BookIssuance.date_issued.isnot(None)).all()

    # Create a defaultdict to store the number of issued books on each date
    issued_dates_counts = defaultdict(int)

    # Count the number of issued books on each date
    for issuance in issuances:
        date_issued = issuance.date_issued.date()  # Extract only the date part
        issued_dates_counts[date_issued] += 1

    # Convert defaultdict to a list of tuples (date, count) sorted by date
    issued_dates_counts_list = sorted(issued_dates_counts.items())

    # Extract dates and counts from the received data
    borrowed_dates = [date for date, _ in issued_dates_counts_list]
    books_borrowed = [count for _, count in issued_dates_counts_list]

    # Convert borrowed_dates to datetime objects
    borrowed_dates = [datetime.strptime(date.strftime('%Y-%m-%d'), '%Y-%m-%d') for date in borrowed_dates]

    # Create a line chart
    plt.figure(figsize=(10, 6))
    plt.plot(borrowed_dates, books_borrowed, marker='o', linestyle='-')
    plt.title('Books Borrowed Over Time')
    plt.xlabel('Date')
    plt.ylabel('Number of Books Borrowed')
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.grid(True)
    chart_filename_2 = f'IssuedBooksOverTime.png'
    chart_path_2 = os.path.join(charts_dir, chart_filename_2)

    # Save the chart as an image or display it
    plt.savefig(chart_path_2, format='png')
    plt.close()

    # Prepare the response data with the relative path to the chart
    dashboard_data = {
        'total_issued_books': total_issued_books,
        'total_sections': total_sections,
        'total_books': total_books,
        'popular_sections': [{'section_id': section.id, 'section_name': section.name} for section in popular_sections],
        'chart_1_image_path': f'static/charts/{chart_filename_1}',
        'chart_2_image_path': f'static/charts/{chart_filename_2}'
    }

    return jsonify(dashboard_data), 200
