#Author: Blanche Chung
#Created Date: Spring 2023
#Description: This file is the views file for the website package. It contains the routes for the webpages.

from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Notary, Document, NotaryDocument, UserDocument
from website import db
from .models import User, Notary, Document, NotaryDocument, UserDocument, FormData

views = Blueprint('views', __name__)


# Create view for index
@views.route('/') 
def home():
    return render_template("index.html")

@views.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    # get user and notary data
    user = User.query.filter_by(id=current_user.id).first()
    notaries = Notary.query.all()

    # get user documents
    user_documents = []
    for user_document in user.user_documents:
        user_documents.append(user_document.document)

    # get notary documents
    notary_documents = []
    for notary in notaries:
        for notary_document in notary.notary_documents:
            notary_documents.append(notary_document.document)

    return render_template("user-account.html", user=user, notaries=notaries, user_documents=user_documents, notary_documents=notary_documents)

# @views.route('/notary/<int:id>', methods=['GET', 'POST'])
# @login_required
# def notary(id):
#     # get notary data
#     notary = Notary.query.filter_by(id=id).first()
#     notary_documents = []
#     for notary_document in notary.notary_documents:
#         notary_documents.append(notary_document.document)

#     return render_template("notary-account.html", notary=notary, notary_documents=notary_documents)

@views.route('/user-homepage', methods=['GET', 'POST'])
@login_required
def user_homepage():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        document_type = request.form['document_type']
        
        # Create FormData object and associate it with the current user
        form_data = FormData(
            first_name=first_name,
            last_name=last_name,
            email=email,
            document_type=document_type,
            user_id=current_user.id
        )

        # Add the FormData object to the database
        db.session.add(form_data)
        db.session.commit()

        return redirect(url_for('user_homepage'))

    return render_template('user-homepage.html', user=current_user)





#Create view for About page
@views.route('/about')
def about():
    return render_template("about.html")

#Create view for Contact page
@views.route('/contact')
def contact():
    return render_template("contact.html")

#Create view for Service page
@views.route('/service')
def service():
    return render_template("service.html")

#create view for pricing page
@views.route('/pricing')
def pricing():
    return render_template("pricing.html")

#create view for 404 page
@views.route('/404')
def error404():
    return render_template("404.html")

#create view for 401 page
@views.route('/401')
def error401():
    return render_template("401.html")

#create view for detail_services page
@views.route('/detail_services')
def detail_services():
    return render_template("detail_services.html")

#create view for reset-password page
@views.route('/reset-password')
def reset_password():
    return render_template("reset-password.html")

#create view for update password page
@views.route('/update-password')
def update_password():
    return render_template("update-password.html")


#create view for access-denied page
@views.route('/access-denied')
def access_denied():
    return render_template("access-denied.html")

@views.route('/.wf_graphql/csrf')
def csrf():
    return jsonify({"data": {"csrfToken": "1234"}})


    













