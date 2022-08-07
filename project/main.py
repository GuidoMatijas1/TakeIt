from . import db
from flask import Blueprint, render_template
from flask_login import login_required, current_user


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html', city=current_user.city)


@main.route('/test')
def test():
    return render_template('test.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)