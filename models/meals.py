from config import db
import matplotlib.pyplot as plt
import numpy as np


class Meals(db.Model):
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(200), nullable=False)
    calorie = db.Column(db.String(200), nullable=False)
    time = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
