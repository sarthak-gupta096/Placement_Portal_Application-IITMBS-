from flask import request, current_app as app
from flask_restful import Resource, Api
from models import db, Users, Company, Student, PlacementDrive, Application
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required


class AdminDashboardAPI(Resource):
    @jwt_required()
    def get(self):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        if not current_user or current_user.role !='admin':
            return {"message":"Access Denied!"},401
        
        total_students = Users.query.filter_by(role='student', status='approved').count()
        total_companies = Users.query.filter_by(role='company', status='approved').count()
        total__approved_drives = PlacementDrive.query.filter_by(status='approved').count()
        return {
            "total_reg_students": total_students,
            "total_reg_companies": total_companies,
            "total_approved_drives": total__approved_drives
        }, 200
    

class PendingStudentsAPI(Resource):
    @jwt_required()
    def get(self):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        
        if not current_user or current_user.role != 'admin':
            return {"message": "Access Denied! Admin only."}, 401
        
    
        pending_students = db.session.query(Users).filter(
            Users.role == 'student',
            Users.status != 'approved'
        ).all()
        
        students_list = []
        for user in pending_students:
            students_list.append({
                "user_id": user.id,
                "email": user.email,
                "full_name": user.student_profile.full_name if user.student_profile else "N/A",
                "roll_number": user.student_profile.roll_number if user.student_profile else "N/A",
                "branch": user.student_profile.branch if user.student_profile else "N/A",
                "cgpa": float(user.student_profile.cgpa) if user.student_profile and user.student_profile.cgpa else 0.0,
                "passout_year": user.student_profile.passout_year if user.student_profile else "N/A",
                "status": user.status
            })
        
        return {
            "message": "Pending student requests",
            "pending_students": students_list
        }, 200


class PendingCompanyAPI(Resource):
    @jwt_required()
    def get(self):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        
        if not current_user or current_user.role != 'admin':
            return {"message": "Access Denied! Admin only."}, 401
        
    
        pending_companies = db.session.query(Users).filter(
            Users.role == 'company',
            Users.status != 'approved'
        ).all()
        
        companies_list = []
        for user in pending_companies:
            companies_list.append({
                "user_id": user.id,
                "name": user.company_profile.name if user.company_profile else "N/A",
                "website": user.company_profile.website if user.company_profile else "N/A",
                "hr_name": user.company_profile.hr_name if user.company_profile else "N/A",
                "hr_contact": float(user.company_profile.hr_contact) if user.company_profile else "N/A",
                "desc": user.company_profile.description if user.company_profile else "N/A",
                "status": user.status
            })
        
        return {
            "message": "Pending company requests",
            "pending_companies": companies_list
        }, 200





class AdminApplicationsAPI(Resource):
    @jwt_required()
    def get(self):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        
        if not current_user or current_user.role != 'admin':
            return {"message": "Access Denied! Admin only."}, 401
        
        # Get all applications
        applications = Application.query.all()
        
        apps_list = []
        for app in applications:
            apps_list.append({
                "application_id": app.id,
                "student_name": app.student.full_name if app.student else "N/A",
                "student_roll": app.student.roll_number if app.student else "N/A",
                "drive_id": app.drive.id if app.drive else "N/A",
                "job_title": app.drive.job_title if app.drive else "N/A",
                "company_name": app.drive.company.name if app.drive and app.drive.company else "N/A",
                "status": app.status,
                "applied_on": app.applied_on.isoformat() if app.applied_on else "N/A"
            })
        
        return {
            "message": "All student applications",
            "applications": apps_list,
            "total_applications": len(apps_list)
        }, 200
