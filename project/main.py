from .models import User
from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user
import flask_sqlalchemy as fs
from . import db

main = Blueprint('main', __name__)


@main.route('/home')
def auth_index():
    return render_template('index.html', name=current_user.name)

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
    return render_template('profile.html', name=current_user.name)


@main.route('/test_page')
def test_page():
    user_list = User.query.all()
    return render_template('test_page.html', items=user_list)