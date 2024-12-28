from flask_mail import Message
import random
import string
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from app.models.user_model import User
from app.extensions import db,bcrypt
from flask_login import login_user
from flask import Flask
from app.utils.send_email import generate_reset_token,send_password_reset_email

auth_bp = Blueprint('auth', __name__,template_folder='app/templates')

# Login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check user in the database
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):  # Using bcrypt to check hashed password
            login_user(user)  # Logs the user in
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard.dashboard'))  # Adjust 'dashboard.home' to your actual home route
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')
# Registration route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        full_name = request.form['full_name']
        email = request.form['email']
        dob = request.form['dob']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate passwords match
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html',errorc = 'Passwords do not match.')

        # Check for existing user
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists.', 'warning')
            return render_template('register.html',erroru = 'Username or email already exists.')
        # Hash the password and create a new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, full_name=full_name, email=email, dob=dob, password=hashed_password,password_hash=hashed_password)

        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    """Logs out the user by clearing their session."""
    # Clear the session data
    session.pop('user_id', None)  # Assuming 'user_id' is stored in session for authentication

    # Optionally, you can add a flash message for user feedback
    # flash('You have been logged out.', 'info')

    # Redirect to the login page after logout
    return redirect(url_for('auth.login'))

@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """Handle the forgot password request."""
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            # Generate a unique token for password reset
            token = generate_reset_token(user)

            # Generate reset link
            reset_link = url_for('auth.reset_password', token=token, _external=True)

            # Send the reset link to the user's email
            send_password_reset_email(user.email, reset_link)

            flash('A password reset link has been sent to your email address.', 'info')
            return redirect(url_for('auth.login'))
        else:
            flash('No account found with that email address.', 'danger')

    return render_template('forgot_password.html')



@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(request.url)

        # Validate token and reset password
        user = User.query.filter_by(reset_token=token).first()
        if user:
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password = hashed_password
            user.reset_token = None  # Invalidate the token
            db.session.commit()
            flash('Password reset successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid or expired token.', 'danger')

    return render_template('forgot_password.html', token=token, otp_sent=True)
