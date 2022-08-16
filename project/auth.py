from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Gmah
from . import db
from flask_login import login_user, login_required, logout_user
import sqlite3
from . import send
auth = Blueprint('auth', __name__)



@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login_gmah')
def login_gmah():
    return render_template('gmah_login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    gmah = Gmah.query.filter_by(email=email).first()
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database

    if user:
        if not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        login_user(user, remember=remember)
        return redirect(url_for('main.auth_index'))
    if gmah:
        if not check_password_hash(gmah.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        login_user(gmah, remember=remember)
        return redirect(url_for('main.auth_index'))
    else:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/user_signup')
def user_signup():
    return render_template('user_signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    id = request.form.get('id')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    phone = request.form.get('phone')
    city = request.form.get('city')
    street = request.form.get('street')
    streetnum = request.form.get('streetnum')
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()  # if this returns a user, then the email already exists in
    # database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(id=id, email=email, password=generate_password_hash(password, method='sha256'), name=firstname ,last_name=lastname,
                    city=city, phone=phone, street=street, street_number=streetnum, is_blocked=0)
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
    id = request.form.get('id')
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    owner_first_name = request.form.get('owner_first_name')
    owner_last_name = request.form.get('owner_last_name')
    phone = request.form.get('phone')
    city = request.form.get('city')
    street = request.form.get('street')
    street_number = request.form.get('street_number')
    category = request.form.get('category')
    password = request.form.get('password')
    gmah = Gmah.query.filter_by(name=name).first()
    if gmah:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.gmah_signup'))

    new_gmah = Gmah(id=id, email=email, name=name, password=generate_password_hash(password, method='sha256'),
                    owner_first_name=owner_first_name, owner_last_name=owner_last_name, phone=phone, city=city,
                    street=street, street_number=street_number, category=category,)


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


@auth.route('/resetpassword', methods=['POST'])
def reset_password():
    email = request.form.get('email')
    id = request.form.get('id')
    user = User.query.filter_by(email=email).first()
    gmah = Gmah.query.filter_by(email=email).first()
    if user:
        user_query = User.query.filter_by(email=email).first()
        user_id = str(user_query.id)
        if user_id == id:
            send.send_mail();
            return "sec"
        else:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.forget'))
    if gmah:
        gmah_query = Gmah.query.filter_by(email=email).first()
        gmah_id = str(gmah_query.id)
        if gmah_id == id:
            return "sendmail-ok"
        else:
            return "sendmail- not   ok"
            # return redirect(url_for('auth.forget'))
