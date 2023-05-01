#Author: Blanche Chung
#Created Date: Spring 2023
#Description: This file is the models file for the website package. It contains the models for the database.

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# Create User class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    user_documents = db.relationship('UserDocument')
    notary_id = db.Column(db.Integer, db.ForeignKey('notary.id'))
    documents = db.relationship('Document', backref='user', lazy=True)


# Create Notary class
class Notary(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    address = db.Column(db.String(150))
    address2 = db.Column(db.String(150))
    city = db.Column(db.String(150))
    state = db.Column(db.String(150))
    zip_code = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    cert_no = db.Column(db.String(150))
    notary_documents = db.relationship('NotaryDocument')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(150))
    encrypted_data = db.Column(db.LargeBinary)  # encrypted data with secure_storage.py
    file = db.Column(db.LargeBinary)
    hash_value = db.Column(db.String(64), nullable=False)  # Add this line to store the hash value
    user_documents = db.relationship('UserDocument')
    notary_documents = db.relationship('NotaryDocument')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)




# Create UserDocument class
class UserDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    notary_id = db.Column(db.Integer, db.ForeignKey('notary.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

# Create NotaryDocument class
class NotaryDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    notary_id = db.Column(db.Integer, db.ForeignKey('notary.id'))
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    document_type = db.Column(db.String(100), nullable=False)
    uploaded_file = db.Column(db.String(255), nullable=False)

    def validate(self):
        if len(self.first_name) < 2:
            raise ValueError("First name must be at least 2 characters long.")
        if len(self.last_name) < 2:
            raise ValueError("Last name must be at least 2 characters long.")
        if not self.email:
            raise ValueError("Email is required.")
        if len(self.document_type) < 2:
            raise ValueError("Document type must be at least 2 characters long.")
        if not self.uploaded_file:
            raise ValueError("File is required.")
