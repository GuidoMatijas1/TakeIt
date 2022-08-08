from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    last_name = db.Column(db.String(1000))
    phone = db.Column(db.String(10))
    city = db.Column(db.String(200))
    street = db.Column(db.String(200))
    street_number = db.Column(db.Integer)
    is_gmah = db.Column(db.Boolean)
    is_blocked = db.Column(db.Boolean)


class Gmah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    owner_first_name = db.Column(db.String(50))
    owner_last_name = db.column(db.String(50))
    phone = db.Column(db.String(10))
    category = db.Column(db.String(50))
    city = db.Column(db.String(200))
    street = db.Column(db.String(200))
    street_number = db.Column(db.Integer)
