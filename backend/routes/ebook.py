# Import necessary modules
from flask import Blueprint, request, jsonify
from flask import current_app as app
from flask_login import login_required, current_user
from models import db, Book, Section
from werkzeug.utils import secure_filename
import os

# Create a Blueprint for book-related APIs
book_api_bp = Blueprint('book_api', __name__)

# API for creating a new book (requires librarian role)
@book_api_bp.route('/add', methods=['POST'])
@login_required
def create_book():
    # Check if the authenticated user is a librarian
    if not current_user.is_librarian:
        return jsonify({'message': 'Unauthorized. Librarian role required.'}), 403

    data = request.form
    book_file = request.files.get('book')  # Access book file
    book_cover = request.files.get('image')
    # Validate required fields
    if not all(field in data for field in ['title', 'author', 'description']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    new_book = Book(
        title=data['title'],
        author=data['author'],
        description=data['description'],
        section_id=data['section']
        # Add other fields as needed
    )

    db.session.add(new_book)
    db.session.flush()
    
    book_filename = secure_filename(str(new_book.id)+'.pdf')
    book_path = os.path.join(app.config['UPLOAD_FOLDER_BOOK'], book_filename)
    book_file.save(book_path)
    book_url = f"/static/books/{book_filename}"
    new_book.file_path = book_url

    if book_cover:
        book_cover_filename = secure_filename(str(new_book.id)+'.jpeg')
        book_cover_path = os.path.join(app.config['UPLOAD_FOLDER_BOOK_COVER'], book_cover_filename)
        book_cover.save(book_cover_path)
        book_cover_url = f"/static/book_covers/{book_cover_filename}"
        new_book.book_cover = book_cover_url
    # Add the new book to the database
    
    db.session.commit()

    return jsonify({'message': 'Book created successfully'}), 201


# API for retrieving a list of all books
@book_api_bp.route('/all', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    book_list = [{'id': book.id, 'title': book.title, 'author': book.author, 'description': book.description, 'book_cover': book.book_cover, 'section': book.section_id} for book in books]
    return jsonify({'books': book_list})


# API for retrieving details of a specific book
@book_api_bp.route('/get_book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    book_details = {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'content': book.content,
        # Include other fields as needed
    }

    return jsonify({'book': book_details})


# API for updating details of a specific book (requires librarian role)
@book_api_bp.route('/update/<int:book_id>', methods=['PUT'])
@login_required
def update_book(book_id):
    # Check if the authenticated user is a librarian
    if not current_user.is_librarian:
        return jsonify({'message': 'Unauthorized. Librarian role required.'}), 403

    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    data = request.form
    book_cover = request.files.get('image')

    # Update fields if provided in the request
    book.title = data['title']
    book.author = data['author']
    book.description = data['description']
    book.section_id=data['section']

    if(book_cover):
        book_cover_filename = secure_filename(str(book_id)+'.jpeg')
        book_cover_path = os.path.join(app.config['UPLOAD_FOLDER_BOOK_COVER'], book_cover_filename)

        try:
            book_cover.save(book_cover_path)
            book_cover_url = f"/static/book_covers/{book_cover_filename}"
            book.book_cover = book_cover_url
            app.logger.info(f"Book cover saved in dir")
        except Exception as e:
            app.logger.error(f"Error saving book cover: {e}")
            return jsonify({'message': 'Error saving book cover'}), 500

    # Commit changes to the database
    db.session.commit()

    return jsonify({'message': 'Book updated successfully'}), 201


# API for deleting a specific book (requires librarian role)
@book_api_bp.route('/delete/<int:book_id>', methods=['DELETE'])
@login_required
def delete_book(book_id):
    # Check if the authenticated user is a librarian
    if not current_user.is_librarian:
        return jsonify({'message': 'Unauthorized. Librarian role required.'}), 403

    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    # Delete the book from the database
    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Book deleted successfully'})

@book_api_bp.route('/search', methods=['GET'])
def search_books():
    # Get the search query from the request parameters
    query = request.args.get('query', '')

    # Perform the search in books based on title, author, and section
    books = Book.query.filter(
        (Book.title.ilike(f'%{query}%')) |
        (Book.author.ilike(f'%{query}%')) |
        (Book.section.has(Section.name.ilike(f'%{query}%')))
    ).all()

    # Prepare the response data
    search_results = [{'id': book.id, 'title': book.title, 'author': book.author, 'section': book.section.name} for book in books]

    return jsonify({'search_results': search_results}), 200