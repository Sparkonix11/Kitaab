from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User
import os

general_user = Blueprint('general_user', __name__)

# API for checking the user's profile (requires authentication)
@general_user.route('/profile', methods=['GET'])
@login_required
def profile():
    # Access the current authenticated user using Flask-Login's current_user
    user = current_user

    # Return user details as JSON
    return jsonify({
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'image': user.image,
    }), 200


@general_user.route('/edit_profile', methods=['POST'])
@login_required
def edit_profile():
    data = request.form
    image_file = request.files.get('image')  # Access image file

    # Check if the required fields are present in the request
    if not any(field in data for field in ['name', 'username', 'email']):
        return jsonify({'message': 'Missing required fields'}), 400

    # Check if the username or email already exists for other users
    if 'username' in data and data['username'] != current_user.username:
        existing_username = User.query.filter_by(username=data['username']).first()
        if existing_username:
            return jsonify({'message': 'Username already exists'}), 409

    if 'email' in data and data['email'] != current_user.email:
        existing_email = User.query.filter_by(email=data['email']).first()
        if existing_email:
            return jsonify({'message': 'Email already exists'}), 409

    # Check if the password is provided for confirmation
    if 'password' not in data:
        return jsonify({'message': 'Password is required for confirmation'}), 400

    # Check if the provided password matches the user's password
    if not check_password_hash(current_user.password, data['password']):
        return jsonify({'message': 'Invalid password for confirmation'}), 401

    # Update user profile information
    current_user.name = data['name']
    current_user.username = data['username']
    current_user.email = data['email']

    # Update the image only if it's sent in the request
    if image_file:
            # Save the image to the static folder
            image_filename = secure_filename(data['username']+'.jpeg')
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_path)
            image_url = f"/static/{image_filename}"
            current_user.image = image_url

    # Commit changes to the database
    db.session.commit()

    user_data = {
            'id': current_user.id,
            'name': current_user.name,
            'username': current_user.username,
            'email': current_user.email,
            'image': current_user.image,
            'role': current_user.role
        }
    
    return jsonify({'message': 'Profile updated successfully', 'user': user_data}), 200


@general_user.route('/change_password', methods=['POST'])
@login_required
def change_password():
    data = request.form()

    # Check if the required fields are present in the request
    if not all(field in data for field in ['current_password', 'new_password', 'confirm_new_password']):
        return jsonify({'message': 'Missing required fields'}), 400

    # Check if the provided current password matches the user's password
    if not check_password_hash(current_user.password, data['current_password']):
        return jsonify({'message': 'Invalid current password'}), 401

    # Check if the new password and confirm new password match
    if data['new_password'] != data['confirm_new_password']:
        return jsonify({'message': 'New passwords do not match'}), 400

    # Update the user's password with the new password
    current_user.password = generate_password_hash(data['new_password'], method='pbkdf2:sha256')

    # Commit changes to the database
    db.session.commit()

    return jsonify({'message': 'Password changed successfully'}), 200

@general_user.route('/book_history', methods=['GET'])
@login_required
def user_book_history():
    # Get all book issuances for the current user
    book_issuances = current_user.book_issuances.all()

    # Prepare the response data
    history_data = []

    for issuance in book_issuances:
        book_data = {
            'book_id': issuance.book.id,
            'book_title': issuance.book.title,
            'date_issued': issuance.date_issued.strftime('%Y-%m-%d %H:%M:%S'),
            'return_date': issuance.return_date.strftime('%Y-%m-%d %H:%M:%S') if issuance.return_date else None,
            'date_read': issuance.date_read.strftime('%Y-%m-%d %H:%M:%S') if issuance.date_read else None,
            'is_returned': issuance.is_returned
        }

        history_data.append(book_data)

    return jsonify({'book_history': history_data}), 200