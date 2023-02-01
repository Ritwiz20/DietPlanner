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


    # def plot_user(goal, calorie, time) :   
        # calorie = np.array(calorie)
        # time = np.array(time)
        
        # plt.scatter(time,calorie, color='red', where=(calorie >= goal))
        # plt.scatter(time,calorie, color='blue', where=(calorie < goal))
        # plt.plot(time,calorie, color='blue', where=(calorie < goal) )
        # plt.plot(time,calorie, color='red', where=(calorie >= goal) )
        # plt.xlabel('Time')
        # plt.ylabel('Calorie')
        # plt.axhline(y=goal, color='red', linestyle='-')
        # plt.title("Plot of calorie intake")

        # return plt.show()