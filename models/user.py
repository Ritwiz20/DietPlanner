from config import db

class User(db.Model):
    __tablename__ = 'user'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(200), nullable=False)

    
    profile =db.relationship('Profile', backref='user')
    plan =db.relationship('Plan', backref='user')
    meals =db.relationship('Meals', backref='user')


    def verify_password(self, passw):
        return self.password==passw