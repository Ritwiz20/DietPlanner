from flask import  Flask, request, jsonify
from flask_cors import CORS
from config import db, SECRET_KEY, my_db
from os import path, getcwd, environ
from dotenv import load_dotenv

import matplotlib.pyplot as plt
import numpy as np


from models.user import User
from models.profile import Profile
from models.plan import Plan
from models.meals import Meals


load_dotenv(path.join(getcwd(), '.env'))

check_id=0
create_db=0


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    app.secret_key = SECRET_KEY

    db.init_app(app)
    print("DB initialized successfully")

    CORS(app)

# Signup, Log-in and Log-out
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



        @app.route("/login", methods=['POST'])
        def login():
            data = request.form.to_dict(flat=True)
            try:
                user = User.query.filter_by(email=data['email']).first()
                if user.verify_password(data['password']):
                    global check_id
                    check_id=user.id
                    return jsonify({'status':'success'})
                else:
                  return jsonify({'status': 'fail'})

            except AttributeError:
                return jsonify({'status':'email not found'})
        

        @app.route('/logout', methods=['POST'])
        def logout():
            global check_id
            if check_id == 0:
                return jsonify({"Error":"Please log in to continue"})
            else :
                check_id=0
                return jsonify({'status':'success'})



#Profile, meal and Plan completion methods
        @app.route('/get_profile', methods=['POST'])
        def get_profile():

            if check_id == 0:
                return jsonify({"Error":"Please log in to continue"})

            user = User.query.filter_by(id = check_id).first()

            data = request.form.to_dict(flat=True)
            new_profile = Profile(
                user_id = user.id,
                age = data['age'],
                gender = data['gender'],
                height = data['height'],
                weight = data['weight'],
                workout = data['workout'],
            )

            db.session.add(new_profile)
            db.session.commit()
            return jsonify({"msg": "Profile updated successfully"})




        @app.route('/create_plan', methods = ['POST'])
        def create_plan():
            if check_id == 0:
                return jsonify({"Error":"Please log in to continue"})            
            

            user = User.query.filter_by(id = check_id).first()

            data = request.form.to_dict(flat=True)
            new_plan = Plan(
                user_id = user.id,
                g_calorie = data['g_calorie'],
                g_weight= data['g_weight'], 
                g_time = data['g_time'],
            )
            db.session.add(new_plan)
            db.session.commit()
            return jsonify({"msg":"Plan created successfully"})




        
        @app.route('/add_meal', methods = ['POST'])
        def add_meal():
            if check_id == 0:
                return jsonify({"Error":"Please log in to continue"})

            user = User.query.filter_by(id = check_id).first()    
            meal_data = request.get_json()   
            for data in meal_data["data"]:
                new_meals = Meals(
                    meal=data["meal"],
                    calorie=data["calorie"],
                    time=data["time"],
                    user_id=user.id
                )
                db.session.add(new_meals)
            db.session.commit()
            return jsonify({"msg":"Meal Added Successfully"})




#Updation of the inserted data
        @app.route("/update_user", methods=['PUT'])
        def update_user():
            if check_id == 0:
                return jsonify({"Error":"Please log in to continue"})            
 
            update_info = request.args.get('update_info')

            user=User.query.filter_by(id = check_id)
            data = request.form.to_dict(flat=True)

            user.update(
                {getattr(User,update_info):data['value']}
            )

            db.session.commit()
            return jsonify({"msg": "User data updated successfully"})





        @app.route('/update_profile', methods=['PUT'])
        def update_profile():
            if check_id == 0:
                return jsonify({"Error":"Please log in to continue"})     

            update_info = request.args.get('update_info')
            user = User.query.filter_by(id = check_id).first()
            profile = Profile.query.filter_by(user_id = user.id)

            data = request.form.to_dict(flat=True)  
            profile.update(
                {getattr(Profile,update_info):data['value']}
            )    

            db.session.commit()
            return jsonify(msg = "Profile updated successfully")



        
        @app.route('/update_plan', methods=['PUT'])
        def update_plan():
            if check_id == 0:
                return jsonify({"Error":"Please log in to continue"})
                
            update_info = request.args.get('update_info')
            user = User.query.filter_by(id = check_id).first()
            plan = Plan.query.filter_by(user_id = user.id)

            data = request.form.to_dict(flat=True)

            plan.update(
                {getattr(Plan,update_info):data['value']}
            )    

            db.session.commit()
            return jsonify(msg = "Plan updated successfully")





#Ploting the data 
        @app.route("/plot_user", methods=['GET'])
        def plot_user():
            if check_id == 0:
                return jsonify({"Error":"Please log in to continue"})

            meals=Meals.query.filter_by(user_id = check_id)
            calorie=[0]
            time=[0]
            cal=0
            for m in meals:
                cal=cal+int(m.calorie)
                calorie.append(cal)
                time.append(int(m.time))

            goal=int(Plan.query.filter_by(user_id=check_id).first().g_calorie)
            # x=Meals.plot_user(goal, calorie, time)

            calorie = np.array(calorie)
            time = np.array(time)

            mask = calorie>=goal

            # plt.plot(time[mask], calorie[mask], color='red')
            # plt.plot(time[~mask], calorie[~mask], color='blue')
            # plt.scatter(time[mask], calorie[mask], color='red')
            # plt.scatter(time[~mask], calorie[~mask], color='blue') 

            plt.plot(time,calorie)
            plt.scatter(time,calorie)
    
            plt.ylabel('Calorie')
            plt.axhline(y=goal, color='red', linestyle='-')
            plt.title("Plot of calorie intake")

            plt.show()
            return jsonify({"Plot":'Graph'})
            

       

#Deletion methods
        @app.route("/delete_user", methods=['POST'])
        def delete_user():
            if check_id == 0:
                return jsonify({"Error":"Please log in to continue"})            
            
            user=User.query.filter_by(id = check_id).first()
            name=user.name
            db.session.delete(user)
            db.session.commit()
            return jsonify({'User': "deleted", "Name": name})

        

        @app.route("/delete_plan", methods=["POST"])
        def delete_plan():
            if check_id == 0:
                return jsonify({"Error":"Please log in to continue"})

            plan=Plan.query.filter_by(user_id = check_id).first()
            db.session.delete(plan)
            db.session.commit()
            return jsonify({'Plan': "deleted"})




        @app.route("/delete_profile", methods=["POST"])
        def delete_profile():
            if check_id == 0:
                return jsonify({"Error":"Please log in to continue"})

            profile=Profile.query.filter_by(user_id = check_id).first()
            db.session.delete(profile)
            db.session.commit()
            return jsonify({'Profile': "deleted"})



        
        @app.route("/delete_meal", methods=["POST"])
        def delete_meal():
            if check_id == 0:
                return jsonify({"Error":"Please log in to continue"})

            name = request.args.get('name')

            meals=Meals.query.filter_by(user_id = check_id)
            for m in meals:
                if m.meal == name:
                    x=1
                    db.session.delete(m)
            
            if x == 1:
                db.session.commit()
                return jsonify({'Meals':"Deleted","Name":name})
            else :
                return jsonify({"Error":"Meal not found"})
        




        if create_db:
            db.drop_all()
            db.create_all()
        db.session.commit()

        return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port='4545', debug=True)
