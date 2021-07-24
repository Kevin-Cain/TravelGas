from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func 
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    userName = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    trip = db.relationship('Trip')

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    MPG = db.Column(db.Integer())
    GasTankCapacity = db.Column(db.Integer())
    HomeAddress = db.Column(db.String(150))
    Destination = db.Column(db.String(150))