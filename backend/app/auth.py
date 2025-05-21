from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from .models import db, AppUser

auth = Blueprint('auth', __name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return AppUser.query.get(int(user_id))

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if user already exists
    if AppUser.query.filter_by(Email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    if AppUser.query.filter_by(Username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400
    
    # Create new user
    new_user = AppUser(
        Username=data['username'],
        PasswordHash=generate_password_hash(data['password']),
        Email=data['email'],
        FirstName=data['first_name'],
        LastName=data['last_name'],
        AddressLine1=data.get('address_line1'),
        AddressLine2=data.get('address_line2'),
        City=data.get('city'),
        PostalCode=data.get('postal_code'),
        Country=data.get('country'),
        PhoneNumber=data.get('phone_number')
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    user = AppUser.query.filter_by(Username=data['username']).first()
    if user and check_password_hash(user.PasswordHash, data['password']):
        login_user(user)
        return jsonify({
            'message': 'Logged in successfully',
            'user': {
                'id': user.UserID,
                'username': user.Username,
                'email': user.Email,
                'first_name': user.FirstName,
                'last_name': user.LastName
            }
        }), 200
    return jsonify({'error': 'Invalid username or password'}), 401

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth.route('/profile')
@login_required
def get_profile():
    return jsonify({
        'id': current_user.UserID,
        'username': current_user.Username,
        'email': current_user.Email,
        'first_name': current_user.FirstName,
        'last_name': current_user.LastName,
        'address_line1': current_user.AddressLine1,
        'address_line2': current_user.AddressLine2,
        'city': current_user.City,
        'postal_code': current_user.PostalCode,
        'country': current_user.Country,
        'phone_number': current_user.PhoneNumber
    }), 200

@auth.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    data = request.get_json()
    
    try:
        for key, value in data.items():
            if key != 'password' and hasattr(current_user, key):
                setattr(current_user, key, value)
        
        if 'password' in data:
            current_user.PasswordHash = generate_password_hash(data['password'])
        
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
