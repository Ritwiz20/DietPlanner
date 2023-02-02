from config import db
class Plan(db.Model):
    __tablename__ = 'plan'
    id = db.Column(db.Integer, primary_key=True)
    g_calorie = db.Column(db.String(200), nullable=False)
    g_weight = db.Column(db.String(200), nullable=False)
    g_time = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    