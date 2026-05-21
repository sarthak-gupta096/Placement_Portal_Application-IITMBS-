from flask import request, current_app as app
from flask_restful import Resource, Api
from models import db, Users, Company, Student
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required

# @app.route('/test_cache')
# # @cache.cached(timeout=10)
# def test_cache():
#     time.sleep(10)
#     return 'Testing is working'





# class WelcomeAPI(Resource):
#     @jwt_required()
#     # @cache.cached(timeout=120)
#     def get(self):
#         return {'message': 'Welcome to Placement Portal App'}, 200
    
#     def post(self):
#         data = request.get_json()
#         name = data.get('name', 'User')
#         msg = f"Hello! {name}"
#         return {'msg': msg}, 200
    

class LoginAPI(Resource):
    def post(self):
        data=request.get_json()
        if not (data.get('email') and data.get('password')):
            return {'message':'Both username & password fields are required!'},400
        user=Users.query.filter_by(email=data.get('email')).first()
        if user:
            if user.password==data.get('password'):
                token=create_access_token(identity=str(user.id))
                return {'message':'User logged In',
                        'token':token,
                        'role':user.role,
                        'status': user.status  
                        },200
            return {'message':'Incorrect password'},400
        return {'message':'User not found!'},400

# 200 ok , 201 create new record , 404 not found, 400 bad request , 401 auth, 403 auth, 405 method not found

class SignupAPI(Resource):
    def post(self):
        data = request.get_json()
        if data.get('email') and data.get('password') and data.get('role'):
            role = data.get('role')

            user=Users.query.filter_by(email=data.get('email')).first()
            if user:
                return {'message':'User already exists!'},400
            
            new_user = Users(email=data.get('email'),password=data.get('password'),
            role=role)
        
            db.session.add(new_user)
            db.session.flush() 

            try:
                if role == 'student':
                    new_student = Student(
                    user_id=new_user.id,
                    full_name=data.get('full_name'),
                    roll_number=data.get('roll_number'),
                    branch=data.get('branch'),
                    cgpa=data.get('cgpa'),
                    passout_year=data.get('passout_year'))
                    db.session.add(new_student)

                elif role == 'company':
                    new_company = Company(
                    user_id=new_user.id,
                    name=data.get('company_name'),
                    website=data.get('website'),
                    hr_name=data.get('hr_name'),
                    hr_contact=data.get('hr_contact'),
                    description=data.get("description"))
                    db.session.add(new_company)

                db.session.commit()
                return {"message": f"{role.capitalize()} signup successfully"}, 201

            except Exception as e:
                db.session.rollback()
                return {"error": str(e)}, 400
        return {'message':'Bad request! All the data fields are required'},400