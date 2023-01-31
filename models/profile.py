from config import db

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(200), nullable=False)
    weight = db.Column(db.String(200), nullable=False)
    height = db.Column(db.String(200), nullable=False)
    workout = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))