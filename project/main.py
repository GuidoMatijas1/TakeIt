from .models import User, Gmah, Products, Borrows, Donations
from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user
import flask_sqlalchemy as fs
from . import db
import sqlite3
import os
import geopy
import folium
from .auth import searchgmahforprod,compare_dates,get_user,get_product
from folium.plugins import FastMarkerCluster


main = Blueprint('main', __name__)


@main.route('/home')
def auth_index():
    return render_template('index.html', name=current_user.name)
# @main.route('/home')
# def auth_index():
#     if current_user.is_active:
#         return "if"
#         # return render_template('index.html')
#     else:
#         return current_user.name
#         # return render_template('index.html', name=current_user.name)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/new')
def index1():
    return render_template('newindex.html')

@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/test')
def test():
    return render_template('test.html')


# @main.route('/user_profile/<email>')
# def user_profile(email):
#     user = User.query.filter_by(email=email).first()
#     gmah=False
#     if not user:
#         gmah=True
#         user = Gmah.query.filter_by(email=email).first()
#     user_id=user.id
#     results = Products.query.filter_by(gmah_id=user_id).all()
#     return render_template('user_profile.html', user=user,results=results, gmah=gmah)


@main.route('/profile/<email>')
def profile(email):
    user = User.query.filter_by(email=email).first()
    gmah=False
    if not user:
        gmah=True
        user = Gmah.query.filter_by(email=email).first()
    user_id=user.id
    results = Products.query.filter_by(gmah_id=user_id).all()
    return render_template('user_profile.html', user=user,results=results, gmah=gmah)


# @main.route('/profile')
# @login_required
# def profile():
#     gmah_id = current_user.id
#     results = Products.query.filter_by(gmah_id=gmah_id).all()
#     return render_template('profile.html',results=results)


@main.route('/test_page')
def test_page():
    gmah_list = Gmah.query.all()
    return render_template('test_page.html', items=gmah_list)

@main.route('/product/<id>')
def product_page(id):
    product = Products.query.filter_by(id=id).all()
    product_gmah = Products.query.filter_by(id=id).first()
    gmah = Gmah.query.filter_by(id=str(product_gmah.gmah_id)).first()
    return render_template('product_page.html', product=product, gmah=gmah,)


@main.route('/donate_product_page/<id>')
@login_required
def donate_product_page(id):
    product = Donations.query.filter_by(id=id).first()
    owner =None
    if product.user_id:
        gmah = Gmah.query.filter_by(id=str(product.user_id)).first()
        if not gmah:
            user = User.query.filter_by(id=str(product.user_id)).first()
            owner = user
        else:
            owner = gmah
    return render_template('donate_product_page.html', product=product,owner=owner)


# @main.route('/gmah_page/<id>')
# def gmah_page(id):
#     gmah = Gmah.query.filter_by(id=id).first()
#     products = Products.query.filter_by(gmah_id=id).all()
#     return render_template('gmah_page.html',gmah=gmah,products=products)


# @main.route('/gmah_search/<id>')
# def gmah_search(id):
#     gmah = Gmah.query.filter_by(id=id).first()
#     return render_template('product_page.html', gmah=gmah)

@main.route('/test_map')
def test_map():
    gmah_list = Gmah.query.all()
    locator = geopy.Nominatim(user_agent="MyGeocoder")
    israel_location = locator.geocode('Tel Aviv')
    map1 = folium.Map(zoom_start=8, location=[israel_location.latitude,israel_location.longitude],prefer_canvas=True        )
    for gmah in gmah_list:
        gmah_adress = str(gmah.street + ' ' + str(gmah.street_number) + ', ' + gmah.city + ', Israel')
        location = locator.geocode(gmah_adress)
        if location:
            folium.Marker([location.latitude, location.longitude], popup=popup(gmah)).add_to(map1)
            map1.save('test_map.html')

    return map1._repr_html_()


# @main.route('/test_map_profile/<email>')
# def test_map_profile(email):
#     test_map_profile    gmah = Gmah.query.filter_by(email=email).first()
#     locator = geopy.Nominatim(user_agent="MyGeocoder")
#     israel_location = locator.geocode('Tel Aviv')
#     gmah_adress = str(gmah.street + ' ' + str(gmah.street_number) + ', ' + gmah.city + ', Israel')
#     location = locator.geocode(gmah_adress)
#     if not location:
#         map1 = folium.Map(zoom_start=9, location=[israel_location.latitude, israel_location.longitude],
#                           prefer_canvas=True)
#     else:
#         map1 = folium.Map(zoom_start=15, location=[location.latitude, location.longitude], prefer_canvas=True)
#     if location:
#         folium.Marker([location.latitude, location.longitude], popup=popup(gmah)).add_to(map1)
#         map1.save('test_map.html')
#
#     return map1._repr_html_()

@main.route('/popup')
def popup(gmah):
    return render_template('map_popup.html', name=gmah.name, city=gmah.city, id=gmah.id, email=gmah.email)


# @main.route('/iframe')
# def iframe(gmah):
#     return flask.send_file('templates/popup_iframe.html', gmah=gmah)


@login_required
@main.route('/gmah_dashboard')
def gmah_dashboard():
    id = current_user.id
    product_name_list = []
    products_dict = {}
    borrowed_products_dict = {}
    available_products_dict = {}
    total_borrows = Borrows.query.filter_by(gmah_id=id).count()
    pending_borrows = Borrows.query.filter_by(gmah_id=id,approved=0,is_active=0).count()
    active_borrows = Borrows.query.filter_by(gmah_id=id, approved=1, is_active=1).count()
    gmah_products = Products.query.filter_by(gmah_id=id).all()
    all_borrows = Borrows.query.filter_by(gmah_id=id).all()
    for product in gmah_products:
        product_name_list.append(product.name)
        all_product = Products.query.filter_by(gmah_id=id).all()
    product_name_list = list(set(product_name_list))
    for product in product_name_list:
        products_dict[product] = Products.query.filter_by(name=product).count()
        borrowed_products_dict[product] = Products.query.filter_by(name=product,idle=1).count()
        available_products_dict[product] = Products.query.filter_by(name=product,idle=0).count()
    return render_template('gmah_dashboard.html', total_borrows=total_borrows,
                           pending_borrows=pending_borrows,
                           active_borrows=active_borrows,
                           product_name_list=product_name_list,
                           products_dict=products_dict,
                           borrowed_products_dict=borrowed_products_dict,
                           available_products_dict=available_products_dict,
                           all_product=all_product,
                           all_borrows=all_borrows,
                           func=get_user,
                           func2=get_product,
                           func3=compare_dates)