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
    mpg = db.Column(db.Integer())
    HomeAddress = db.Column(db.String(150))
    Destination = db.Column(db.String(150))
    fuel = db.Column(db.Integer())
    time = db.Column(db.String(150))
    distance = db.Column(db.Float())
    cost = db.Column(db.Float())

    mondayMaxTemp = db.Column(db.Integer())
    mondayMinTemp = db.Column(db.Integer())
    mondayIcon = db.Column(db.String(150))
    mondayDescription = db.Column(db.String(150))

    tuesdayMaxTemp = db.Column(db.Integer())
    tuesdayMinTemp = db.Column(db.Integer())
    tuesdayIcon = db.Column(db.String(150))
    tuesdayDescription = db.Column(db.String(150))

    wensdayMaxTemp = db.Column(db.Integer())
    wensdayMinTemp = db.Column(db.Integer())
    wensdayIcon = db.Column(db.String(150))
    wensdayDescription = db.Column(db.String(150))

    thursdayMaxTemp = db.Column(db.Integer())
    thursdayMinTemp = db.Column(db.Integer())
    thursdayIcon = db.Column(db.String(150))
    thursdayDescription = db.Column(db.String(150))

    fridayMaxTemp = db.Column(db.Integer())
    fridayMinTemp = db.Column(db.Integer())
    fridayIcon = db.Column(db.String(150))
    fridayDescription = db.Column(db.String(150))

    saturdayMaxTemp = db.Column(db.Integer())
    saturdayMinTemp = db.Column(db.Integer())
    saturdayIcon = db.Column(db.String(150))
    saturdayDescription = db.Column(db.String(150))

    sundayMaxTemp = db.Column(db.Integer())
    sundayMinTemp = db.Column(db.Integer())
    sundayIcon = db.Column(db.String(150))
    sundayDescription = db.Column(db.String(150))

