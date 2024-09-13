# Import necessary modules
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, Section

# Create a Blueprint for section-related APIs
section_api_bp = Blueprint('section_api', __name__)

# API for creating a new section (requires librarian role)
@section_api_bp.route('/add', methods=['POST'])
@login_required
def create_section():
    # Check if the authenticated user is a librarian
    if not current_user.is_librarian:
        return jsonify({'message': 'Unauthorized. Librarian role required.'}), 403

    data = request.get_json()

    # Validate required fields
    if not all(field in data for field in ['name', 'description']):
        return jsonify({'message': 'Missing required fields'}), 400

    new_section = Section(
        name=data['name'],
        description=data['description'],
        # Add other fields as needed
    )

    # Add the new section to the database
    db.session.add(new_section)
    db.session.commit()

    return jsonify({'message': 'Section created successfully'}), 201


# API for retrieving a list of all sections
@section_api_bp.route('/all', methods=['GET'])
def get_all_sections():
    sections = Section.query.all()
    section_list = []
    for section in sections:
        books = [{'id': book.id, 'title': book.title, 'author': book.author, 'description': book.description} for book in section.books]
        section_data = {
            'id': section.id,
            'name': section.name,
            'description': section.description,
            'books': books
        }
        section_list.append(section_data)
    return jsonify({'sections': section_list})


# API for retrieving details of a specific section
@section_api_bp.route('/get_section/<int:section_id>', methods=['GET'])
def get_section(section_id):
    section = Section.query.get(section_id)
    if not section:
        return jsonify({'message': 'Section not found'}), 404

    section_details = {
        'id': section.id,
        'name': section.name,
        'description': section.description,
        # Include other fields as needed
    }

    return jsonify({'section': section_details})


# API for updating details of a specific section (requires librarian role)
@section_api_bp.route('/update/<int:section_id>', methods=['PUT'])
@login_required
def update_section(section_id):
    # Check if the authenticated user is a librarian
    if not current_user.is_librarian:
        return jsonify({'message': 'Unauthorized. Librarian role required.'}), 403

    section = Section.query.get(section_id)
    if not section:
        return jsonify({'message': 'Section not found'}), 404

    data = request.get_json()

    # Update fields if provided in the request
    if 'name' in data:
        section.name = data['name']
    if 'description' in data:
        section.description = data['description']
    # Update other fields as needed

    # Commit changes to the database
    db.session.commit()

    return jsonify({'message': 'Section updated successfully'})


# API for deleting a specific section (requires librarian role)
@section_api_bp.route('/delete/<int:section_id>', methods=['DELETE'])
@login_required
def delete_section(section_id):
    # Check if the authenticated user is a librarian
    if not current_user.is_librarian:
        return jsonify({'message': 'Unauthorized. Librarian role required.'}), 403

    section = Section.query.get(section_id)
    if not section:
        return jsonify({'message': 'Section not found'}), 404

    # Delete the section from the database
    db.session.delete(section)
    db.session.commit()

    return jsonify({'message': 'Section deleted successfully'})
