from flask import request, current_app as app
from flask_restful import Resource, Api
from models import db, Users, Company, Student, PlacementDrive, Application
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required
from task import data_export
from flask import current_app






class StudentDashboardAPI(Resource):
    @jwt_required()
    def get(self):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        
        if not current_user or current_user.role != 'student':
            return {"message": "Access Denied!"}, 401

        student = current_user.student_profile

        all_drives = PlacementDrive.query.filter_by(status='approved').all()
        eligible_drives = []
        for drive in all_drives:
            branches = drive.eligible_branches.split(",")

            if (
                student.cgpa >= drive.min_cgpa
                and student.branch in branches
                and drive.year_start <= student.passout_year <= drive.year_end
            ):
                eligible_drives.append(drive)
        
        drives = []
        for drive in all_drives:
            drives.append({
                "drive_id": drive.id,
                "job_title": drive.job_title,
                "company_name": drive.company.name,
                "salary": drive.salary,
                "location": drive.location,
                "deadline": drive.deadline,
                "min_cgpa": drive.min_cgpa,
                "eligible_branches": drive.eligible_branches
            })
        
        return drives, 200





# to show all approved students on admin dash

class StudentAPI(Resource):

    @jwt_required()
    def get(self):

        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)

        if current_user.role == "student":
            student = current_user.student_profile
            if not student:
                return {"message": "Student profile not found"}, 404

            return {
                "full_name": student.full_name,
                "roll_number": student.roll_number,
                "branch": student.branch,
                "cgpa": student.cgpa,
                "passout_year": student.passout_year,
                "resume": student.resume
            }, 200


        elif current_user.role == "admin":
            # students = Student.query.all()
            students = Users.query.filter_by(
            role="student",
            status="approved"
        ).all()

        result = []

        for user in students:

            student = user.student_profile

            if not student:
                continue

            result.append({
                "user_id": user.id,
                "full_name": student.full_name,
                "roll_number": student.roll_number,
                "branch": student.branch,
                "cgpa": student.cgpa,
                "passout_year": student.passout_year,
                "status": user.status,
                "is_active": user.is_active
            })

            return {"registered-students": result}, 200

    
    @jwt_required()
    def put(self):

        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)

        if not current_user or current_user.role != 'student':
            return {"message": "Access Denied! Student only."}, 401

        student = current_user.student_profile

        data = request.get_json()

        student.full_name = data.get('full_name', student.full_name)
        student.roll_number = data.get('roll_number', student.roll_number)
        student.branch = data.get('branch', student.branch)
        student.cgpa = data.get('cgpa', student.cgpa)
        student.passout_year = data.get('passout_year', student.passout_year)
        student.resume = data.get('resume', student.resume)

        db.session.commit()

        return {"message": "Profile updated successfully!"}, 200
    
    @jwt_required()
    def delete(self,user_id):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        if not current_user or current_user.role !='admin':
            return {"message":"Access Denied!"},401

        student=Users.query.get(user_id)
        if not student:
            return {'message':'Student not found!'},404

        db.session.delete(student)
        db.session.commit()
        return {"message":"Student Profile Rejected Successfully!"},200
    
    @jwt_required()
    def patch(self, user_id):
        current_user = Users.query.get(get_jwt_identity())
        if not current_user or current_user.role != 'admin':
            return {"message": "Access Denied!"}, 401
        
        target_user = Users.query.get(user_id)
        if target_user:
            target_user.status = 'approved'
            db.session.commit()
            return {"message": "Student Profile Approved Successfully!"}
        return {"message": "User not found"}, 404
    
class SearchStudentsAPI(Resource):

    @jwt_required()
    def get(self):

        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)

        # Only admin allowed
        if not current_user or current_user.role != "admin":
            return {"message": "Access Denied! Admin only."}, 401

        search = request.args.get("search")

        query = Student.query

        if search:
            query = query.filter(Student.full_name.ilike(f"%{search}%"))

        students = query.all()

        result = []

        for s in students:
            result.append({
                "user_id": s.user.id,
                "full_name": s.full_name,
                "roll_number": s.roll_number,
                "branch": s.branch,
                "cgpa": s.cgpa,
                "passout_year": s.passout_year,
                "status": s.user.status,
                "is_active": s.user.is_active
            })

        return {
            "message": "Students Search Result",
            "students": result
        }, 200









class StudProfileAPI(Resource):
    @jwt_required()
    def patch(self,user_id):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        if not current_user or current_user.role !='admin':
            return {"message":"Access Denied!"},401
        
        current_stud=Users.query.get(user_id)

        data = request.get_json()
        action = data.get('action')
        if action == 'active':
            current_stud.is_active = True
            db.session.commit()
            return {"message":"Student Reactivated Successfully!"}
        
        elif action == 'blacklist':
            current_stud.is_active = False
            db.session.commit()
            return {"message":"Student Blacklisted Successfully!"}
        


class ExportedDataAPI(Resource):
    @jwt_required()
    def get(self):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        if not current_user or current_user.role != 'student':
            return {"message": "Access Denied! Student only."}, 401
    
        student = current_user.student_profile
        if not student:
            return {"message": "Student profile not complete!"}, 404
        
        history = []
        for app in student.applications:
            if app.drive.status == 'closed' or app.status in ['Shortlisted', 'Rejected']:
                history.append({
                    "student_id": student.id,
                    "company_name": app.drive.company.name,
                    "job_title": app.drive.job_title,
                    "status": app.status,
                    "applied_on": app.applied_on.isoformat()
                })
        
        data_export.delay(history, current_user.email)
        return {"message":"Your data exported task has been initiated, Please check your inbox."}, 200