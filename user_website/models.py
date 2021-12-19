from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_reading = db.Column(db.Integer)
    current_reading = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    surcharge = db.Column(db.Integer)
    Phone_number = db.Column(db.String(13))
    text_id = db.Column(db.String(150))
