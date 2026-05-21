from flask import Flask,request
from flask_restful import Resource,Api
import redis
import os
import time
from models import db,Users
from datetime import timedelta
from flask_jwt_extended import JWTManager
from login_api import SignupAPI, LoginAPI
from student_api import StudentAPI, StudProfileAPI, StudentDashboardAPI, ExportedDataAPI, SearchStudentsAPI
from company_api import CompanyAPI, CompProfileAPI, CompanyDashboardAPI, SearchCompaniesAPI
from admin_api import AdminDashboardAPI, AdminApplicationsAPI, PendingStudentsAPI, PendingCompanyAPI
from drive_api import CreateDriveAPI, ApplyDriveAPI, CompanyDrivesAPI
from applications_api import CompanyApplicationsAPI, UpdateApplicationStatusAPI, StudentApplicationsAPI, StudentPlacementHistoryAPI, AllApplicationsAPI
# from worker import celery
from worker import celery_init_app, celery_app
from flask_cors import CORS 



base_dir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
# CORS(app)
# CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
CORS(
    app,
    resources={r"/*": {"origins": "http://localhost:5173"}},
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"]
)

project_root = os.path.abspath(os.path.join(base_dir, '..'))  # Going one level up from backend
instance_folder = os.path.join(project_root, 'instance')

if not os.path.exists(instance_folder):
    os.makedirs(instance_folder)

db_path = os.path.join(instance_folder, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config["SECRET_KEY"] = "super-secret"
app.config["JWT_SECRET_KEY"] = "ppaproject"
app.config["JWT_ACCESS_TOKEN_EXPIRES"]=timedelta(hours=12)

app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = '127.0.0.1'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
app.config['CACHE_REDIS_URL'] = "redis://localhost:6379"

app.config.update(
    CELERY=dict(
        broker_url='redis://localhost:6379/0',
        result_backend='redis://localhost:6379/0',
        task_ignore_result=True,
    ),
)


db.init_app(app)
api=Api(app)


jwt=JWTManager(app)

# cache.init_app(app)
celery_init_app(app)
from task import daily_remainder




with app.app_context():
    db.create_all()

    existing_admin = Users.query.filter_by(role='admin').first()
    if not existing_admin:
        default_username = 'admin@gmail.com'
        default_password = 'password' 

        # hashed_password = generate_password_hash(default_password)
        default_admin = Users(email=default_username, password=default_password,role='admin')
        db.session.add(default_admin)
        db.session.commit()



# @app.route('/test_cache')
# @cache.cached(timeout=10)
# def test_cache():
#     time.sleep(10)
#     return f"Testing is working {time.time()}"









api.add_resource(SignupAPI, '/api/signup')
api.add_resource(PendingStudentsAPI, '/api/admin/pending-students')
api.add_resource(PendingCompanyAPI, "/api/admin/pending-companies")
api.add_resource(SearchStudentsAPI, "/api/admin/search-students")
api.add_resource(SearchCompaniesAPI, "/api/admin/search-companies")
api.add_resource(LoginAPI, '/api/login',methods=['POST'])
api.add_resource(StudentAPI, '/api/student' , '/api/student/<int:user_id>', '/api/admin/registered-students')
api.add_resource(CompanyAPI, '/api/company' , '/api/company/<int:user_id>', '/api/admin/registered-companies')
api.add_resource(CompProfileAPI, '/api/company/status/<int:user_id>')
api.add_resource(StudProfileAPI, '/api/student/status/<int:user_id>')
api.add_resource(AdminDashboardAPI, '/api/admin/dashboard')
api.add_resource(CreateDriveAPI, '/drives', '/drives/<int:drive_id>', methods=['GET','POST', 'PUT', 'PATCH'])
api.add_resource(CompanyDashboardAPI, '/api/company-dashboard')
api.add_resource(StudentDashboardAPI, '/student-dashboard')
api.add_resource(AdminApplicationsAPI, '/admin/applications')
api.add_resource(ApplyDriveAPI, '/apply/<int:drive_id>')
api.add_resource(CompanyApplicationsAPI, '/company/applications')
api.add_resource(UpdateApplicationStatusAPI, '/company/applications/<int:app_id>')
api.add_resource(StudentApplicationsAPI, '/student/applications')
api.add_resource(StudentPlacementHistoryAPI, '/student/history')
api.add_resource(ExportedDataAPI, '/api/history/export')
api.add_resource(CompanyDrivesAPI, "/api/company/<int:company_user_id>/drives")
api.add_resource(AllApplicationsAPI, "/admin/all_applications")

if __name__=='__main__':
    app.run(debug=True)