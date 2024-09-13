# Import necessary modules
from flask import Blueprint, request, jsonify, session
from flask import current_app as app
from datetime import datetime, timedelta
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import base64
from models import db, User

# Create a Blueprint for user-related APIs
auth_api_bp = Blueprint('auth_api', __name__)
# API for user registration (signup)
@auth_api_bp.route('/signup', methods=['POST'])
def signup():
    data = request.form  # Access form data
    image_file = request.files.get('image')  # Access image file

    # Check if the required fields are present in the request
    required_fields = ['name', 'username', 'email', 'password', 'confirm_password']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400

    # Check if the password and confirm_password match
    if data['password'] != data['confirm_password']:
        return jsonify({'message': 'Passwords do not match'}), 400

    # Check if the username or email already exists
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 409

    existing_email = User.query.filter_by(email=data['email']).first()
    if existing_email:
        return jsonify({'message': 'Email already exists'}), 409

    # Handle image upload
    if image_file:
        # Save the image to the static folder
        image_filename = secure_filename(data['username']+'.jpeg')
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        image_file.save(image_path)
        image_url = f"/static/{image_filename}"
    else:
        # Use the default image if no image is provided
        image_url = '/static/user_placeholder.png'

    # Create a new user
    new_user = User(
        name=data['name'],
        username=data['username'],
        email=data['email'],
        password=generate_password_hash(data['password'], method='pbkdf2:sha256'),  # Hash the password
        image=image_url,
        last_login = datetime.utcnow()
    )

    # Add the user to the database
    db.session.add(new_user)
    db.session.commit()

    # Log the user in after signup
    login_user(new_user, remember=True)
    user_data = {
            'id': new_user.id,
            'name': new_user.name,
            'username': new_user.username,
            'email': new_user.email,
            'image': new_user.image,
            'role': "user"
            # Add more user attributes if needed
        }

    return jsonify({'message': 'User created successfully', 'user': user_data}), 201


# API for user login
@auth_api_bp.route('/login', methods=['POST'])
def login():
    data = request.form

    # Check if the required fields are present in the request
    if not all(field in data for field in ['username', 'password']):
        app.logger.error('Missing required fields in login request')
        return jsonify({'message': 'Missing required fields'}), 400

    # Perform user authentication
    user = User.query.filter_by(username=data['username']).first()

    if user and check_password_hash(user.password, data['password']):
        app.logger.info(f'User {user.username} authenticated successfully')
        user.last_login = datetime.utcnow()
        db.session.commit()
        # Log the user in using Flask-Login
        login_user(user, remember=True)
        app.logger.info('User logged in successfully')

        user_data = {
            'id': user.id,
            'name': user.name,
            'username': user.username,
            'email': user.email,
            'image': user.image,
            'role': user.role
        }
        return jsonify({'message': 'Login successful', 'user': user_data}), 200
    else:
        app.logger.error('Invalid credentials provided for login')
        return jsonify({'message': 'Invalid credentials'}), 401


@auth_api_bp.route('/logout', methods=['POST'])
def logout():
    # Check if the user is authenticated
    if current_user.is_authenticated:
        # Log the user out using Flask-Login
        logout_user()
        app.logger.info('User logged out successfully')
        return jsonify({'message': 'Logout successful'}), 200
    else:
        app.logger.error('User not authenticated during logout')
        return jsonify({'message': 'User not authenticated'}), 401
    


