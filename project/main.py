from .models import User, Gmah, Products
from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user
import flask_sqlalchemy as fs
from . import db
import sqlite3
import os
import geopy
import folium

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


@main.route('/user_profile/<email>')
def user_profile(email):
    user = User.query.filter_by(email=email).first()
    return render_template('profile.html', user=user)

@main.route('/profile')
@login_required
def profile():
    gmah_list = Gmah.query.all()
    return render_template('profile.html', items=gmah_list)


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


@main.route('/gmah_page/<id>')
def gmah_page(id):
    gmah = Gmah.query.filter_by(id=id).first()
    products = Products.query.filter_by(gmah_id=id).all()
    return render_template('gmah_page.html',gmah=gmah,products=products)


@main.route('/gmah_search/<id>')
def gmah_search(id):
    gmah = Gmah.query.filter_by(id=id).first()
    return render_template('product_page.html', gmah=gmah)

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

@main.route('/popup')
def popup(gmah):
    return render_template('map_popup.html', name=gmah.name, city=gmah.city, id=gmah.id)

# @main.route('/iframe')
# def iframe(gmah):
#     return flask.send_file('templates/popup_iframe.html', gmah=gmah)
