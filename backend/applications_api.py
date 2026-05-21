from flask import request, current_app as app
from flask_restful import Resource, Api
from models import db, Users, Company, Student, PlacementDrive, Application
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required
from flask import current_app




class CompanyApplicationsAPI(Resource):
    @jwt_required()
    def get(self):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        
        if not current_user or current_user.role != 'company':
            return {"message": "Access Denied! Company only."}, 401
        
        current_company = current_user.company_profile
        if not current_company:
            return {"message": "Company profile not found!"}, 404
        
        apps_list = []
        for drive in current_company.drives:           # Relationship from Company model
            for app in drive.applications:              # Relationship from PlacementDrive
                apps_list.append({
                    "application_id": app.id,
                    "student_name": app.student.full_name,
                    "student_roll": app.student.roll_number,
                    "student_cgpa": app.student.cgpa,
                    "job_title": drive.job_title,
                    "status": app.status,
                    "applied_on": app.applied_on.isoformat()
                })
        
        return apps_list, 200

class UpdateApplicationStatusAPI(Resource):
    @jwt_required()
    def patch(self, app_id):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        
        if not current_user or current_user.role != 'company':
            return {"message": "Access Denied! Company only."}, 401
        
        app = Application.query.get(app_id)
        if not app:
            return {"message": "Application not found!"}, 404
        
        
        data = request.get_json()
        status = data.get('status')
        valid_statuses = ['applied', 'Shortlisted', 'Waiting', 'Rejected']

        if status not in valid_statuses:
            return {"message": "Invalid status"}, 400

        
        app.status = status
        db.session.commit()
        
        return {
            "message": "Application Status updated successfully!",
            "application_id": app.id,
            "new_status": app.status
        }, 200

class AllApplicationsAPI(Resource):

    @jwt_required()
    def get(self):

        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)

        if not current_user or current_user.role != 'admin':
            return {"message": "Access Denied! Admin only."}, 401

        applications = Application.query.all()

        result = []

        for app in applications:
            result.append({
                "application_id": app.id,
                "student_name": app.student.full_name,
                "roll_number": app.student.roll_number,
                "company_name": app.drive.company.name,
                "job_title": app.drive.job_title,
                'department':app.student.branch,
                "status": app.status,
                "applied_on": app.applied_on.strftime("%Y-%m-%d"),
                "resume": app.student.resume
            })

        return {"applications": result}, 200



class StudentApplicationsAPI(Resource):
    @jwt_required()
    def get(self):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        
        if not current_user or current_user.role != 'student':
            return {"message": "Access Denied! Student only."}, 401
        
        student = current_user.student_profile
        if not student:
            return {"message": "Student profile not complete!"}, 404
        
        apps_list = []
        for app in student.applications:                     # Backref from Student model
            apps_list.append({
                "application_id": app.id,
                "job_title": app.drive.job_title,
                "company_name": app.drive.company.name,
                "status": app.status,
                "applied_on": app.applied_on.strftime("%Y-%m-%d"),
                "deadline": app.drive.deadline.strftime("%Y-%m-%d")
            })
        
        return {
            "my_applications": apps_list,
            "total": len(apps_list)
        }, 200



class StudentPlacementHistoryAPI(Resource):
    @jwt_required()
    def get(self):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        
        if not current_user or current_user.role != 'student':
            return {"message": "Access Denied! Student only."}, 401
        
        student = current_user.student_profile
        if not student:
            return {"message": "Student profile not complete!"}, 404
        
        # Past placements: CLOSED drives OR final statuses
        history = []
        for app in student.applications:  
            if app.drive.status == 'closed' or app.status in ['Shortlisted', 'Rejected']:
                history.append({
                    "application_id": app.id,
                    "company_name": app.drive.company.name,
                    "job_title": app.drive.job_title,
                    "status": app.status,
                    "applied_on": app.applied_on.strftime("%Y-%m-%d"),
                    "drive_status": app.drive.status,
                    "salary": str(app.drive.salary) + (' LPA'),
                    "location": app.drive.location
                })
        
        return {
            "placement_history": history,
            "total_past_placements": len(history)
        }, 200
