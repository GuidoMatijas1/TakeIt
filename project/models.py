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
    profile_picture = db.Column(db.String(200))

class Gmah(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(1000))
    password = db.Column(db.String(100))
    owner_first_name = db.Column(db.String(50))
    owner_last_name = db.Column(db.String(50))
    phone = db.Column(db.String(10))
    category = db.Column(db.String(50))
    city = db.Column(db.String(200))
    street = db.Column(db.String(200))
    street_number = db.Column(db.Integer)
    profile_picture = db.Column(db.String(200))

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    category = db.Column(db.String(50))
    description = db.Column(db.String(1000))
    idle = db.Column(db.Boolean)
    gmah_id = db.Column(db.Integer, db.ForeignKey('Gmah.id'))

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    category = db.Column(db.String(50))
    description = db.Column(db.String(1000))
    idle = db.Column(db.Boolean)
    gmah_id = db.Column(db.Integer, db.ForeignKey('Gmah.id'))
    pic_name = db.Column(db.String(50))

class Borrows(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    borrower_id = db.Column(db.Integer)
    gmah_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    approved = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)