from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Entry(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.Date)
    description = db.Column(db.String(10000))
    amount = db.Column(db.Float)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(150),unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    entry = db.relationship('Entry')
