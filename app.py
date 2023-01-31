from flask import  Flask, request, jsonify
from flask_cors import CORS
from config import db, SECRET_KEY
from os import path, getcwd, environ
from dotenv import load_dotenv

from models.user import User
from models.profile import Profile
from models.plan import Plan
from models.meals import Meals


load_dotenv(path.join(getcwd(), '.env'))

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    app.secret_key = SECRET_KEY


    db.init_app(app)
    print("DB initialized successfully")

    CORS(app)


    with app.app_context():
        @app.route('/signup', methods=['POST'])
        def signup():
            data = request.form.to_dict(flat=True)

            new_user = User(
                name = data['name'],
                email = data['email'],
                password = data['password'],
                phone_number = data['phone_number']
            )

            db.session.add(new_user)
            db.session.commit()
            return jsonify(msg = "User signed up successfully")



        # db.drop_all()
        # db.create_all()
        db.session.commit()

        return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port='4545', debug=True)
