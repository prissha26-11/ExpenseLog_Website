from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#entry_category = db.Table('entry_category',
#    db.Column('entry_id',db.Integer,db.ForeignKey('entry.id')),
#    db.Column('category_id',db.Integer,db.ForeignKey('category.id'))
#)

class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    categoryType = db.Column(db.String(500))
    entries = db.relationship('Entry', backref='category')

class Entry(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.Date)
    description = db.Column(db.String(10000))
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'))
    amount = db.Column(db.Integer)
    notes = db.Column(db.String(10000))
    people_id = db.Column(db.Integer,db.ForeignKey('people.id'))

class People(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    image_file = db.Column(db.String(150))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    entry = db.relationship('Entry')
    total = db.Column(db.Numeric(10,2))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(150),unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    people = db.relationship('People')
