from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Gmah, Products
from . import db, mail
from flask_login import login_user, login_required, logout_user
import sqlite3 , string, random
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os

auth = Blueprint('auth', __name__)



@auth.route('/donate_money')
def donate_money():
    return render_template('donate_money.html')


# @auth.route('/donate_money/<id>', methods=['POST'])
# def upload_file(id):
#     user = User.query.filter_by(id=id).first()
#     gmah = Gmah.query.filter_by(id=id).first()
#     if user and request.method == 'POST':
#         f = request.files['file']
#         f.save(os.path.join('project/static/images',secure_filename(f.filename)))
#         user.profile_picture = f.filename
#         db.session.commit()
#         return "gooda"
#     else:
#
#         return "gooda"


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
    password_repeat = request.form.get('password-repeat')
    if password!=password_repeat:
        flash('passwords dont match')
        return render_template('user_signup.html')
    f = request.files['file']
    user_id = User.query.filter_by(id=id).first()  # if this returns a user, then the email already exists in
    # database
    user_email = User.query.filter_by(email=email).first()  # if this returns a user, then the email already exists in

    if user_id or user_email:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('User already exists - Try forget password')
        return redirect(url_for('auth.login'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    f.filename = id + "profile_picture.jpeg"
    f.save(os.path.join('project/static/images/profile/', secure_filename(f.filename)))
    new_user = User(id=id, email=email, password=generate_password_hash(password, method='sha256'), name=firstname ,last_name=lastname,
                    city=city, phone=phone, street=street, street_number=streetnum, is_blocked=0, profile_picture= f.filename)
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
    f = request.files['file']
    password_repeat = request.form.get('password-repeat')
    if password != password_repeat:
        flash('passwords dont match')
        return render_template('gmah_signup.html')
    gmah_id = Gmah.query.filter_by(id=id).first()
    gmah_email = Gmah.query.filter_by(email=email).first()
    if gmah_id:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('ID already exists - Try forget password')
        return redirect(url_for('auth.login'))
    if gmah_email:
        flash('Email already exists - Try forget password')
        return redirect(url_for('auth.login'))
    f.filename = id + "profile_picture.jpeg"
    f.save(os.path.join('project/static/images/profile/', secure_filename(f.filename)))
    new_gmah = Gmah(id=id, email=email, name=name, password=generate_password_hash(password, method='sha256'),
                    owner_first_name=owner_first_name, owner_last_name=owner_last_name, phone=phone, city=city,
                    street=street, street_number=street_number, category=category,profile_picture= f.filename)

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
            return redirect(url_for('auth.forget_send_mail',user_id=str(user_id)))
        else:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.forget'))
    if gmah:
        gmah_query = Gmah.query.filter_by(email=email).first()
        gmah_id = str(gmah_query.id)
        if gmah_id == id:
            return redirect(url_for('auth.forget_send_mail',user_id=str(gmah_id)))
        else:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.forget'))



@auth.route("/forget_send_mail/<user_id>" )
def forget_send_mail(user_id):
   # msg = Message('Hello', sender = 'takeitapp0@gmail.com', recipients = ['guyshmuel93@gmail.com','adiben@mta.ac.il',
   #                                                                       'nofarvi@mta.ac.il','guidoma@mta.ac.il'])
   user_query = User.query.filter_by(id=user_id).first()
   gmah_query = Gmah.query.filter_by(id=user_id).first()
   if user_query:
        randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=9))
        password=generate_password_hash(randomstr, method='sha256')
        user_query.password = password
        db.session.commit()
   else:
        randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=9))
        password = generate_password_hash(randomstr, method='sha256')
        gmah_query.password = password
        db.session.commit()
   msg = Message('Hello', sender = "'TakeIt'<#{takeitapp0@gmail.com}>", recipients = ['guyshmuel93@gmail.com'])
   msg.body = "Your new password is: " +str(randomstr)
   mail.send(msg)
   return redirect(url_for('auth.login'))

# /* Search */
@auth.route('/search', methods=["GET"])
def custom_search():
    categories = db.session.query(Gmah.category).distinct(Gmah.category)

    return render_template("custom_search.html",categories=categories)

@auth.route('/searchgmahbycategory', methods=["POST"])
def searchgmahbycategory():
    serched = request.form.get('search')
    result = Gmah.query.filter_by(category=serched)
    return render_template("gmah_results.html", results=result)

@auth.route('/searchgmahbycity', methods=["POST"])
def searchgmahbycity():
    serched = request.form.get('search')
    # result = Gmah.query.filter_by(city=serched)
    result = Gmah.query.filter(Gmah.city.like('%'+serched+'%')).order_by(Gmah.city)
    return render_template("gmah_results.html", results=result)


# Create Search Function
@auth.route('/search', methods=["POST"])
def search():
    serched = request.form.get('search')
    # result = Products.query.filter_by(name=serched)
    result = Products.query.filter(Products.name.like('%'+serched+'%')).order_by(Products.name)
    return render_template("product_results.html", results=result,func=searchgmahforprod)

@auth.route('/searchgmahforprod/<id>')
def searchgmahforprod(id):
    product_id = Products.query.filter_by(id=id).first()
    gmah_id = product_id.gmah_id
    gmah = Gmah.query.filter_by(id=gmah_id).first()
    if gmah_id:
        return (str(gmah.city)+" "+ str(gmah.street)+" "+str(gmah.street_number))
    else:
        return ""

@auth.route('/my_products/')
def my_products():
    products = Products.query.all()
    return render_template("my_products.html",products=products)


@auth.route('/tests/')
def tests():
    # result = Products.query.with_entities(Products.category).distinct()
    result = db.session.query(Products.category).distinct(Products.category)
    return render_template("custom_search.html",products=result)
