from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Gmah
from . import db
from flask_login import login_user, login_required, logout_user
import sqlite3
auth = Blueprint('auth', __name__)



@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.auth_index'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/user_signup')
def user_signup():
    return render_template('user_signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    city = request.form.get('city')
    # is_gmah = request.form.get('is_gmah')
    # if is_gmah == 'true':
    #     is_gmah = True
    # else:
    #     is_gmah = False
    # return str(password)
    user = User.query.filter_by(email=email).first()  # if this returns a user, then the email already exists in
    # database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), city=city,)
                    # is_gmah=is_gmah)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    if new_user.is_gmah:
        return redirect(url_for('auth.gmah_signup'))

    return redirect(url_for('auth.login'))


@auth.route('/gmah_signup')
def gmah_signup():
    return render_template('gmah_signup.html')


@auth.route('/gmah_signup', methods=['POST'])
def gmah_signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    phone = request.form.get('phone')
    city = request.form.get('city')
    street = request.form.get('street')
    street_number = request.form.get('street_number')
    category = request.form.get('category')
    owner_first_name = request.form.get('owner_first_name')
    owner_last_name = request.form.get('owner_last_name')
    gmah = Gmah.query.filter_by(name=name).first()
    if gmah:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.gmah_signup'))

    new_gmah = Gmah(email=email,
                    name=name,
                    password=generate_password_hash(password, method='sha256'),
                    phone=phone,
                    city=city,
                    street=street,
                    street_number=street_number,
                    category=category,
                    owner_first_name=owner_first_name,
                    owner_last_name=owner_last_name)

    db.session.add(new_gmah)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/forget')
def forget():
    return render_template('forget_password.html')