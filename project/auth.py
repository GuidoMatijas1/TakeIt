import flask_login
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Gmah, Products, Borrows, Donations
from . import db, mail
from flask_login import login_user, login_required, logout_user, current_user
import sqlite3, string, random
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os
import pandas as pd
from datetime import datetime, timedelta
import geopy

auth = Blueprint('auth', __name__)

msg = ""


@auth.route('/donate_money')
def donate_money():
    return render_template('donate_money.html')


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


@auth.route('/update_information/')
def update_information():
    return render_template('update_information.html')


@auth.route('/update_information/', methods=['POST'])
def update_information_post():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    phone = request.form.get('phone')
    city = request.form.get('city')
    street = request.form.get('street')
    streetnum = request.form.get('streetnum')
    email = request.form.get('email')
    users = User.query.filter_by(id=current_user.id).first()
    gmahs = Gmah.query.filter_by(id=current_user.id).first()
    if users:
        if firstname:
            user = User.query.filter_by(id=current_user.id).first()
            user.name = firstname
            db.session.commit()
        if lastname:
            user = User.query.filter_by(id=current_user.id).first()
            user.last_name = lastname
            db.session.commit()
        if phone:
            user = User.query.filter_by(id=current_user.id).first()
            user.phone = phone
            db.session.commit()
        if city:
            user = User.query.filter_by(id=current_user.id).first()
            user.city = city
            db.session.commit()
        if street:
            user = User.query.filter_by(id=current_user.id).first()
            user.street = street
            db.session.commit()
        if streetnum:
            user = User.query.filter_by(id=current_user.id).first()
            user.streetn_number = streetnum
            db.session.commit()
        if email:
            # gmah_email = Gmah.query.filter_by(email=email).first()
            user_email = User.query.filter_by(email=email).first()
            if user_email:
                flash('This Email addresses allready exist.')
                return render_template('/update_information.html')
            else:
                user = User.query.filter_by(id=current_user.id).first()
                user.email = email
                db.session.commit()
    if gmahs:
        if firstname:
            user = Gmah.query.filter_by(id=current_user.id).first()
            user.name = firstname
            db.session.commit()
        if lastname:
            user = Gmah.query.filter_by(id=current_user.id).first()
            user.last_name = lastname
            db.session.commit()
        if phone:
            user = Gmah.query.filter_by(id=current_user.id).first()
            user.phone = phone
            db.session.commit()
        if city:
            user = Gmah.query.filter_by(id=current_user.id).first()
            user.city = city
            db.session.commit()
        if street:
            user = Gmah.query.filter_by(id=current_user.id).first()
            user.street = street
            db.session.commit()
        if streetnum:
            user = Gmah.query.filter_by(id=current_user.id).first()
            user.streetn_number = streetnum
            db.session.commit()
        if email:
            gmah_email = Gmah.query.filter_by(email=email).first()
            if gmah_email:
                flash('This Email addresses allready exist.')
                return render_template('/update_information.html')
            else:
                user = Gmah.query.filter_by(id=current_user.id).first()
                user.email = email
                db.session.commit()
    return render_template('index.html')


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
    if password != password_repeat:
        flash('passwords dont match')
        return render_template('user_signup.html')
    f = request.files['file']
    user_id = User.query.filter_by(id=id).first()  # if this returns a user, then the email already exists in
    # database
    user_email = User.query.filter_by(email=email).first()  # if this returns a user, then the email already exists in
    gmah_email =  Gmah.query.filter_by(email=email).first()
    if gmah_email:
        flash('Email related to Gmah - please sign up with different email')
        return redirect(url_for('auth.login'))
    if user_id or user_email:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('User already exists - Try forget password')
        return redirect(url_for('auth.login'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    f.filename = id + "profile_picture.jpeg"
    f.save(os.path.join('project/static/images/profile/', secure_filename(f.filename)))
    new_user = User(id=id, email=email, password=generate_password_hash(password, method='sha256'), name=firstname,
                    last_name=lastname,
                    city=city, phone=phone, street=street, street_number=streetnum, is_blocked=0,
                    profile_picture=f.filename)
    # is_gmah=is_gmah)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # if new_user.is_gmah:
    #     return redirect(url_for('auth.gmah_signup'))

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
    locator = geopy.Nominatim(user_agent="MyGeocoder")
    gmah_adress = str(street + ' ' + str(street_number) + ', ' + city + ', Israel')
    location = locator.geocode(gmah_adress)
    if not location:
        flash(
            'Your address has spelling error, please check the correct city/street name so you will appear in the map')
        return render_template('gmah_signup.html')
    else:
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
                        street=street, street_number=street_number, category=category, profile_picture=f.filename)

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
            return redirect(url_for('auth.forget_send_mail', user_id=str(user_id)))
        else:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.forget'))
    if gmah:
        gmah_query = Gmah.query.filter_by(email=email).first()
        gmah_id = str(gmah_query.id)
        if gmah_id == id:
            return redirect(url_for('auth.forget_send_mail', user_id=str(gmah_id)))
        else:
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.forget'))


@auth.route("/forget_send_mail/<user_id>")
def forget_send_mail(user_id):
    # msg = Message('Hello', sender = 'takeitapp0@gmail.com', recipients = ['guyshmuel93@gmail.com','adiben@mta.ac.il',
    #                                                                       'nofarvi@mta.ac.il','guidoma@mta.ac.il'])
    user_query = User.query.filter_by(id=user_id).first()
    gmah_query = Gmah.query.filter_by(id=user_id).first()
    if user_query:
        randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=9))
        password = generate_password_hash(randomstr, method='sha256')
        user_query.password = password
        db.session.commit()
        recipient = user_query.email
    else:
        randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=9))
        password = generate_password_hash(randomstr, method='sha256')
        gmah_query.password = password
        db.session.commit()
        recipient = gmah_query.email

    msg = Message('Hello', recipients=[recipient])
    msg.body = 'Your new password is: ' + str(randomstr)
    # msg.html = '<p>This is a test email!</p>'
    mail.send(msg)
    # msg = Message('Hello', sender = "'TakeIt'<#{takeitapp0@gmail.com}>", recipients = ['guyshmuel93@gmail.com'])
    # msg.body = "Your new password is: " +str(randomstr)
    # mail.send(msg)
    return redirect(url_for('auth.login'))


# /*
# */
@auth.route('/search', methods=["GET"])
def custom_search():
    categories = db.session.query(Gmah.category).distinct(Gmah.category)

    return render_template("custom_search.html", categories=categories)


@auth.route('/searchgmahbycategory', methods=["POST"])
def searchgmahbycategory():
    serched = request.form.get('search')
    result = Gmah.query.filter_by(category=serched)
    return render_template("gmah_results.html", results=result)


@auth.route('/searchgmahbycity', methods=["POST"])
def searchgmahbycity():
    serched = request.form.get('search')
    # result = Gmah.query.filter_by(city=serched)
    result = Gmah.query.filter(Gmah.city.like('%' + serched + '%')).order_by(Gmah.city)
    return render_template("gmah_results.html", results=result)


# @auth.route('/search_all', methods=["POST"])
# def search_all():
#     serched = request.form.get('search')
#     # result = Products.query.filter_by(name=serched)
#     result = Products.query.filter(Products.name.like('%'+serched+'%')).order_by(Products.name)
#     result2 = Gmah.query.filter(Gmah.name.like('%' + serched + '%')).order_by(Gmah.name)
#     return render_template("search_all.html", results=result,func=searchgmahforprod,header="Results Page", results2 = result2)

@auth.route('/searchforproduct', methods=["POST"])
def searchforproduct():
    serched = request.form.get('search')
    result = Products.query.filter(Products.name.like('%' + serched + '%')).order_by(Products.name)
    return render_template("product_results.html", results=result, func=searchgmahforprod, header="Results Page")


# Create Search Function
@auth.route('/search', methods=["POST"])
def search():
    serched = request.form.get('search')
    gmah = Gmah.query.filter(Gmah.name.like('%' + serched + '%')).order_by(Gmah.name)
    result = Products.query.filter(Products.name.like('%' + serched + '%')).order_by(Products.name)
    categories = Gmah.query.filter(Gmah.category.like('%' + serched + '%')).order_by(Gmah.category)
    cities = Gmah.query.filter(Gmah.city.like('%' + serched + '%')).order_by(Gmah.city)
    return render_template("product_results.html", results=result, results2=gmah, results3=categories, results4=cities,
                           func=searchgmahforprod, header="Results Page")


@auth.route('/searchgmahforprod/<id>')
def searchgmahforprod(id):
    product_id = Products.query.filter_by(id=id).first()
    gmah_id = product_id.gmah_id
    gmah = Gmah.query.filter_by(id=gmah_id).first()
    if gmah_id:
        return (str(gmah.city) + " " + str(gmah.street) + " " + str(gmah.street_number))
    else:
        return ""


@auth.route('/get_user/<id>')
def get_user(id):
    user = User.query.filter_by(id=id).first()
    return user

@auth.route('/get_product/<id>')
def get_product(id):
    product = Products.query.filter_by(id=id).first()
    return product


@auth.route('/my_products/')
def my_products():
    gmah_id = current_user.id
    gmah = Gmah.query.filter_by(id=gmah_id).first()
    results = Products.query.filter_by(gmah_id=gmah_id).all()
    # return render_template("my_products.html",products=products)
    return render_template("my_products.html", results=results, func=searchgmahforprod, header="My Products")


@auth.route('/tests/')
def tests():
    date = "2023-01-01"
    now = datetime.now()
    now = now.strftime("%Y-%m-%d")
    result = now > date
    if result:
        return "1"
    else:
        return "0"



@auth.route('/borrow_item', methods=['POST'])
@login_required
def borrow_item():
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    gmah_id = request.form.get('gmah_id')
    product_id = request.form.get('product_id')
    borrower_id = current_user.id
    # borrow_id = str(borrower_id) + str(product_id) + str(gmah_id)
    # borrow_id = int(borrow_id)
    # check_id = Borrows.query.filter_by(id=borrow_id).first()
    today = datetime.now()
    try:
        check_start_date = pd.to_datetime(start_date)
    except:
        flash('check your start date and try again')
        return redirect(url_for('main.product_page', id=product_id))
    try:
        check_end_date = pd.to_datetime(end_date)
    except:
        flash('check your end date and try again')
        return redirect(url_for('main.product_page', id=product_id))
    check_start_date = pd.to_datetime(start_date)
    check_end_date = pd.to_datetime(end_date)
    if check_start_date<today:
        flash('Start date cannot be earlier than today')
        return redirect(url_for('main.product_page', id=product_id))
    if check_end_date<check_start_date:
        flash('End date cannot be earlier than start date')
        return redirect(url_for('main.product_page', id=product_id))
    # # while check_id:
    #     borrow_id = borrow_id + 1
    #     check_id = Borrows.query.filter_by(id=borrow_id).first()
    id = random_with_N_digits(5)
    existing_borrow = Borrows.query.filter_by(id=id).first()
    while existing_borrow:
        id = random_with_N_digits(5)
        existing_borrow = Borrows.query.filter_by(id=id).first()

    new_borrow = Borrows(product_id=product_id,
                         gmah_id=gmah_id,
                         borrower_id=borrower_id,
                         start_date=pd.to_datetime(start_date),
                         end_date=pd.to_datetime(end_date),
                         approved=0,
                         is_active=1,
                         declined =  0,
                         id=id)
    if not check_dates(new_borrow):
        borrow = Borrows.query.filter_by(product_id=product_id).first()
        flash('This product isnt available between the dates.' + str(borrow.start_date) + ' and ' + str(borrow.end_date))
        return redirect(url_for('main.product_page', id=product_id))
    db.session.add(new_borrow)
    try:
        db.session.commit()
    except:
        flash('check your end date and try again')
        return redirect(url_for('main.product_page', id=product_id))
    product = Products.query.filter_by(id=product_id).first()
    user = User.query.filter_by(id=borrower_id).first()
    user_name = user.name
    gmah = Gmah.query.filter_by(id=gmah_id).first()
    gmah_mail = gmah.email

    msg = Message('Hello', recipients=[gmah_mail])
    msg.body = "You've just got request for Item:" + str(
        product.name) + " for the dates: " + start_date + " to " + end_date + ". \n By the user " + user_name + "for approve: http://takeit.lol/borrows/"
    mail.send(msg)
    flash('Borrow request send to Gmah owner.We send you email as soon as he reply')
    return render_template('index.html')


@auth.route('/add_product/')
@login_required
def add_product():
    return render_template("add_product.html")


@auth.route('/add_product/', methods=["POST"])
@login_required
def add_product_post():
    name = request.form.get('name')
    gmah_id = request.form.get('gmah_id')
    category = request.form.get('category')
    description = request.form.get('description')
    f = request.files['file']
    profile_picture = f.filename
    f.save(os.path.join('project/static/images/products/', secure_filename(f.filename)))
    check_id = Products.query.filter_by(id=gmah_id).first()
    while check_id:
        new_id = check_id.id + 1
        check_id = Products.query.filter_by(id=new_id).first()
    new_product = Products(name=name,
                           category=category,
                           description=description,
                           gmah_id=gmah_id,
                           idle=1,
                           pic_name=f.filename,
                           id=check_id)
    db.session.add(new_product)
    db.session.commit()
    gmah = Gmah.query.filter_by(id=gmah_id).first()
    user = gmah
    results = Products.query.filter_by(gmah_id=gmah_id).all()
    return render_template('user_profile.html', user=user, results=results, gmah=gmah)
    # return render_template("profile.html")


@auth.route('/borrows/')
@login_required
def borrows():
    gmah_id = current_user.id
    gmah = Gmah.query.filter_by(id=gmah_id).first()
    if not gmah:
        flash('To see all of your borrows please login')
        return redirect(url_for('auth.login'))
    else:
        borrows = Borrows.query.filter_by(gmah_id=gmah_id).all()
        # borrows = Borrows.query.all()
        date = datetime.now()
        date = date.strftime("%Y-%m-%d")
        return render_template("my_borrows.htm", gmah=gmah, borrows=borrows, func=return_user, func2=return_product,
                               date=date,
                               func3=compare_dates)


# @auth.route('/approve_borrow/')
# @login_required
# def approve_borrow():
#     gmah_id = current_user.id
#     gmah = Gmah.query.filter_by(id=gmah_id).first()
#     if not gmah:
#         flash('To see all of your borrows please login')
#         return redirect(url_for('auth.login'))
#     else:
#         borrows = Borrows.query.filter_by(gmah_id=gmah_id).all()
#         date = datetime.now()
#         date = date.strftime("%Y-%m-%d")
#         return render_template("approve_borrow.html", gmah=gmah, borrows=borrows, func=return_user, func2=return_product,
#                                date=date)


@auth.route('/approved_borrow/<id>')
@login_required
def approved_borrow_post(id):
    borrows = Borrows.query.filter_by(id=id).first()
    borrows.approved = 1
    product_id = borrows.product_id
    product = Products.query.filter_by(id=product_id).first()
    product.idle = 0
    db.session.commit()
    user_id = borrows.borrower_id
    user = User.query.filter_by(id=user_id).first()
    user_mail = user.email
    msg = Message('Hello', recipients=[user_mail])
    msg.body = "Your borrow request hab been accetpted!! \n The borrow of the product " + product.name + " for the dates: " + str(
        borrows.start_date) + " to " + str(borrows.end_date)
    mail.send(msg)
    return redirect(url_for('auth.borrows'))


@auth.route('/decline_borrow_post/<id>')
@login_required
def decline_borrow_post(id):
    borrows = Borrows.query.filter_by(id=id).first()
    borrows.declined = 1
    db.session.commit()
    product_id = borrows.product_id
    product = Products.query.filter_by(id=product_id).first()
    user_id = borrows.borrower_id
    user = User.query.filter_by(id=user_id).first()
    user_mail = user.email
    msg = Message('Hello', recipients=[user_mail])
    msg.body = "Your borrow request hab been rejected!! \n The borrow of the product " + product.name + " for the dates: " + str(
        borrows.start_date) + " to " + str(borrows.end_date)
    mail.send(msg)
    return redirect(url_for('auth.borrows'))




@auth.route('/return_user/<id>')
def return_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return user
    else:
        return ""


@auth.route('/return_gmah/<id>')
def return_gmah(id):
    gmah = Gmah.query.filter_by(id=id).first()
    if gmah:
        return gmah
    else:
        return ""


@auth.route('/return_product/<id>')
def return_product(id):
    product = Products.query.filter_by(id=id).first()
    if product:
        return product
    else:
        return ""


@auth.route('/compare_dates/<date>')
def compare_dates(date):
    date = date.strftime("%Y-%m-%d")
    now = datetime.now()
    now = now.strftime("%Y-%m-%d")
    result = now < date
    if result:
        return False
    else:
        if now == date:
            return True
        else:
            return False


def check_dates(borrow):
    product_id = borrow.product_id
    existing_borrow = Borrows.query.filter_by(product_id=product_id,approved=1).first()
    if existing_borrow:
        current_start = pd.to_datetime(existing_borrow.start_date)
        current_end = pd.to_datetime(existing_borrow.end_date)
        requested_start = pd.to_datetime(borrow.start_date)
        requested_end = pd.to_datetime(borrow.end_date)
        if (current_start < requested_start and current_end > requested_start) or (
                current_start < requested_end and current_end > requested_end) or (
                current_start > requested_start and current_end < requested_end):
            return False
    return True


@auth.route('/donate_items/')
def donate_items():
    gmah_list = Gmah.query.all()
    return render_template('donate_items.html', gmah_list=gmah_list)


@auth.route('/donate_items/', methods=["POST"])
def donate_items_post():
    name = request.form.get('name')
    user_id = request.form.get('user_id')
    description = request.form.get('description')
    donate_name = request.form.get('donate_name')
    donate_phone = request.form.get('donate_phone')
    gmah_id = request.form.get('gmah_id')
    f = request.files['file']
    if not f:
        flash('Upload photo is mandatory.')
        return redirect(url_for('auth.donate_items'))
    _picture = f.filename
    f.save(os.path.join('project/static/images/products/', secure_filename(f.filename)))
    today = datetime.now()
    id = 1;
    check_id = Donations.query.filter_by(id=id).first()
    while check_id:
        id = id + 1
        check_id = Donations.query.filter_by(id=id).first()
    if donate_phone:
        new_product = Donations(id=id,
                                name=name,
                                description=description,
                                upload_date=today,
                                is_available=1,
                                pic_name=f.filename,
                                donate_name=donate_name,
                                donate_phone=donate_phone,
                                donate_for = gmah_id,
                                accepted=0,
                                )

    else:
        new_product = Donations(id=id,
                                name=name,
                                description=description,
                                upload_date=today,
                                is_available=1,
                                pic_name=f.filename,
                                user_id=user_id,
                                donate_for=gmah_id,
                                accepted=0,
                                )

    db.session.add(new_product)
    db.session.commit()
    return render_template('donate_items.html')


@auth.route('/dashboard/')
def dashboard():
    gmah_id = current_user.id
    gmah = Gmah.query.filter_by(id=gmah_id).first()
    borrows_list = Borrows.query.filter_by(gmah_id=gmah_id).all()
    product_list = Products.query.filter_by(gmah_id=gmah_id).all()
    return render_template('dashboard.html', gmah=gmah, id=gmah_id, borrows=borrows_list, products=product_list)


@auth.route('/dashboard_borrows/', methods=["POST"])
def dashboard_borrows():
    return str(current_user)
    # borrows = Borrows.query.filter_by(gmah_id=current_user.id).all()
    # render_template('donate_items.html',borrows=borrows)


@auth.route('/donations')
def donations():
    id = current_user.id
    results = Donations.query.filter_by(donate_for=id,accepted=0)
    # result = Products.query.filter_by(name=serched)
    return render_template("donations.html", results=results, func=get_user, header="Item For Donations")


@auth.route('/accept_donation/<id>')
def accept_donation(id):
    donation = Donations.query.filter_by(id=id).first()
    donation.accepted = 1
    db.session.commit()
    # result = Products.query.filter_by(name=serched)
    return redirect(url_for('auth.donations'))


@auth.route('/end_borrow/<id>')
def end_borrow(id):
    borrows = Borrows.query.filter_by(id=id).first()
    borrows.approved = 0
    borrows.is_active = 0
    product_id = borrows.product_id
    product = Products.query.filter_by(id=product_id).first()
    product.idle = 1
    db.session.commit()
    user_id = borrows.borrower_id
    user = User.query.filter_by(id=user_id).first()
    user_mail = user.email
    gmah_id = borrows.gmah_id
    gmah = Gmah.query.filter_by(id=gmah_id).first()
    gmah_mail = gmah.email
    msg = Message('Hello', recipients=[user_mail])
    msg.body = "Your borrow has ended!! \n for product " + product.name + "\nYou can see this mail as returning confirmation\n we like to see you aggin."
    mail.send(msg)
    msg = Message('Hello', recipients=[gmah_mail])
    msg.body = "The borrow of item: " + product.name + " has been ended.\n the product is back to inventory"
    mail.send(msg)
    return redirect(url_for('auth.borrows'))


@auth.route('/start_borrow/<id>')
def start_borrow(id):
    borrows = Borrows.query.filter_by(id=id).first()
    borrows.approved = 1
    borrows.is_active = 1
    product_id = borrows.product_id
    product = Products.query.filter_by(id=product_id).first()
    product.idle = 0
    db.session.commit()
    user_id = borrows.borrower_id
    user = User.query.filter_by(id=user_id).first()
    user_mail = user.email
    gmah_id = borrows.gmah_id
    gmah = Gmah.query.filter_by(id=gmah_id).first()
    gmah_mail = gmah.email
    msg = Message('Hello', recipients=[user_mail])
    msg.body = "Your borrow has started!! \n for product " + product.name + "\nwe remined you that the borrow approved until to: "+ str(borrows.end_date)
    mail.send(msg)
    msg = Message('Hello!', recipients=[gmah_mail])
    msg.body = "The borrow of item: " + product.name +" number "+str(product.id)+ " has been started.\n the product is out of stock until "+str(borrows.end_date)
    mail.send(msg)
    return redirect(url_for('auth.borrows'))

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)
