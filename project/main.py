from .models import User, Gmah
from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user
import flask_sqlalchemy as fs
from . import db
import sqlite3
import os

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
    return render_template('test_page.html', name=current_user.name)


@main.route('/test_page')
def test_page():
    user_list = User.query.filter_by(name="Guy")
    # this_name=str(current_user.name)
    # product_test = User.query.filter_by(name=current_user.name).first()
    # user_list = User.query.filter_by(name=product_test.name)

    return render_template('test_page.html', items=user_list)