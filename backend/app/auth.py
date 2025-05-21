from flask import Blueprint, request, jsonify, flash, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from .models import db, AppUser, CustomerOrder

bp = Blueprint('auth', __name__)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return AppUser.query.get(int(user_id))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        data = request.form
        
        # Check if user already exists
        if AppUser.query.filter_by(Email=data['email']).first():
            flash('Email already registered', 'error')
            return redirect(url_for('auth.register'))
        if AppUser.query.filter_by(Username=data['username']).first():
            flash('Username already taken', 'error')
            return redirect(url_for('auth.register'))
        
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
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('auth.register'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        data = request.form
        
        user = AppUser.query.filter_by(Username=data['username']).first()
        if user and check_password_hash(user.PasswordHash, data['password']):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main_routes.index'))
        flash('Invalid username or password', 'error')
        return redirect(url_for('auth.login'))

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('main_routes.index'))

@bp.route('/profile')
@login_required
def get_profile():
    return render_template('profile.html', user=current_user)

@bp.route('/profile', methods=['PUT'])
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

@bp.route('/order_history')
@login_required
def order_history():
    """Display user's order history."""
    try:
        orders = CustomerOrder.query.filter_by(UserID=current_user.UserID).order_by(CustomerOrder.OrderDate.desc()).all()
        return render_template('order_history.html', orders=orders)
    except Exception as e:
        flash('Could not load order history. Please try again later.', 'error')
        return redirect(url_for('main_routes.index'))
