#Author: Blanche Chung
#Created Date: Spring 2023
#Description: This file is the auth file for the website package. It contains the routes for the login, 
#logout, sign up, delete account, and change password pages.

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from .models import User, Notary, Document, NotaryDocument, UserDocument, FormData
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import os
from . import login_manager



auth = Blueprint('auth', __name__)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get data from form
        email = request.form.get('email')
        password = request.form.get('password')

        # check if user exists
        user = User.query.filter_by(email=email).first()
        if user:
            # check if password is correct
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('view.user_homepage'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("log-in.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # get data from form
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # check if user exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password != confirm_password:
            flash('Passwords do not match.', category='error')
        elif len(password) < 7:
            flash('Password must be greater than 6 characters.', category='error')
        else:
            # add new user to database
            new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            # Print statements to check if the user is being added to the database
            print('New user added to database!')
            print('User ID:', new_user.id)
            print('User email:', new_user.email)

            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('auth.login'))

    return render_template("signup.html", user=current_user)



@auth.route('/delete-account', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'POST':
        # get data from form
        email = request.form.get('email')
        password = request.form.get('password')

        # check if user exists
        user = User.query.filter_by(email=email).first()
        if user:
            # check if password is correct
            if check_password_hash(user.password, password):
                db.session.delete(user)
                db.session.commit()
                flash('Account deleted.', category='success')
                return redirect(url_for('auth.login'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("delete_account.html", user=current_user)

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        # get data from form
        email = request.form.get('email')
        old_password = request.form.get('oldPassword')
        new_password1 = request.form.get('newPassword1')
        new_password2 = request.form.get('newPassword2')

        # check if user exists
        user = User.query.filter_by(email=email).first()
        if user:
            # check if password is correct
            if check_password_hash(user.password, old_password):
                # check if new passwords match
                if new_password1 != new_password2:
                    flash('New passwords do not match.', category='error')
                elif len(new_password1) < 7:
                    flash('New password must be greater than 6 characters.', category='error')
                else:
                    user.password = generate_password_hash(new_password1, method='sha256')
                    db.session.commit()
                    flash('Password changed.', category='success')
                    return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("change_password.html", user=current_user)

#Create a view for Document
@auth.route('/document', methods=['GET', 'POST'])
@login_required
def document():
    if request.method == 'POST':
        # get data from form
        document_type = request.form.get('Document-Type')
        uploaded_file = request.files['uploaded_file']

        # Save the uploaded file
        file_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(file_path)

        # Add new Document to the database
        new_document = Document(document_type=document_type, uploaded_file=file_path, user_id=current_user.id)
        db.session.add(new_document)
        db.session.commit()

        return redirect(url_for('document'))

    return render_template('document.html')
