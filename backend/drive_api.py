from flask import request, current_app as app
from flask_restful import Resource, Api
from models import db, Users, Company, Student, PlacementDrive, Application
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required
from datetime import datetime
from flask import current_app


class CreateDriveAPI(Resource):

    @jwt_required()
    def get(self, drive_id=None):

        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)

        if not current_user:
            return {"message": "Access Denied!"}, 401

        if drive_id:

            drive = PlacementDrive.query.get(drive_id)
            if not drive:
                return {"message": "Drive not found!"}, 404

            applicants = []

            for app in drive.applications:
                student = app.student

                applicants.append({
                    "application_id": app.id,
                    "name": student.full_name,
                    "email": student.user.email,
                    "branch": student.branch,
                    "cgpa": student.cgpa,
                    'resume':student.resume
                })

            return {
                "drive": {
                    "drive_id": drive.id,
                    "job_title": drive.job_title,
                    "description": drive.desc,
                    "location": drive.location,
                    "package": drive.salary,
                    "min_cgpa": drive.min_cgpa,
                    "deadline": drive.deadline.strftime("%Y-%m-%d") if drive.deadline else None,
                    "eligible_branches": drive.eligible_branches,
                    "year_start": drive.year_start,
                    "year_end": drive.year_end,
                    "status": drive.status
                },
                "applicants": applicants
            }, 200


        # getting all drives

        closed_drives=[]
        if current_user.role == "admin":
            drives = PlacementDrive.query.all()

        elif current_user.role == "company":
            company = Company.query.filter_by(user_id=id_from_token).first()
            drives = PlacementDrive.query.filter_by(company_id=company.id).all()

        elif current_user.role == "student":
            drives = PlacementDrive.query.filter_by(status="approved").all()

        else:
            return {"message": "Unauthorized role!"}, 403

        result = []

        for drive in drives:
            result.append({
                "drive_id": drive.id,
                "company_name": drive.company.name,
                "job_title": drive.job_title,
                "location":drive.location,
                'package':drive.salary,
                "status": drive.status,
                "deadline": drive.deadline.strftime("%Y-%m-%d") if drive.deadline else None
            })

        
        return {
            "total_drives": len(result),
            "drives": result
        }, 200

    @jwt_required()
    def post(self):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        if not current_user or current_user.role !='company':
            return {"message":"Access Denied!"},401
        
        company = Company.query.filter_by(user_id=id_from_token).first()
        data = request.get_json()

        try:
            title = data.get('job_title')
            desc = data.get('description')
            deadline_str = data.get('deadline')
            deadline = None

            if deadline_str:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            location=data.get("location")
            min_cgpa = float(data.get('min_cgpa') or 0)
            salary = int(data.get('package') or 0)
            year_start = int(data.get('year_start'))
            year_end = int(data.get('year_end'))

            eligible_branches = data.get('eligible_branches', [])

            if isinstance(eligible_branches, list):
                eligible_branches = ",".join(eligible_branches)

        except (ValueError, TypeError):
            return {"message": "Invalid input data!"}, 400
        
        if not title or not year_start or not year_end:
            return {"message": "Required fields missing!"}, 400

        new_drive = PlacementDrive(
            company_id=company.id,
            job_title=title,
            desc=desc,
            deadline=deadline,
            min_cgpa=min_cgpa,
            eligible_branches=eligible_branches,
            salary=salary,
            location=location,
            year_start=year_start,
            year_end=year_end
        )
        
        db.session.add(new_drive)
        db.session.commit()

        return {"message": "New Drive created successfully!"}, 200
    
    @jwt_required()
    def put(self, drive_id):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        if not current_user or current_user.role != 'company':
            return {'message': 'Access Denied!'}, 401
    
        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return {'message': 'Drive not found!'}, 404
    
        if drive.company.user_id != id_from_token:
            return {'message': 'Access Denied! Can only update own drives.'}, 401
    
        data = request.get_json()
        if not data:
            return {'message': 'No input data provided!'}, 400
    
        drive.job_title = data.get('title', drive.job_title)
        drive.desc = data.get('desc', drive.desc)
        drive.deadline = data.get('deadline', drive.deadline)
        drive.min_cgpa = data.get('min_cgpa', drive.min_cgpa)
        drive.eligible_branches = data.get('eligible_branches', drive.eligible_branches)
        drive.salary = data.get('salary', drive.salary)
        drive.location = data.get('location', drive.location)
        drive.year_start = data.get('year_start', drive.year_start)
        drive.year_end = data.get('year_end', drive.year_end)
    
        db.session.commit()
        return {'message': 'Drive updated successfully!', 'drive_id': drive.id}, 200
    
    @jwt_required()
    def patch(self, drive_id):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)

        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return {'message': 'Drive not found!'}, 404

        data = request.get_json()
        action = data.get('action') if data else None

        if current_user.role == 'admin':

            if drive.status != 'pending':
                return {'message': 'Drive already processed!'}, 400

            if action == 'approve':
                drive.status = 'approved'

            elif action == 'reject':
                drive.status = 'rejected'

            else:
                return {'message': 'Valid action required: approve or reject'}, 400

        elif current_user.role == 'company':

            company = Company.query.filter_by(user_id=id_from_token).first()

            if drive.company_id != company.id:
                return {'message': 'Can only modify own drives'}, 401

            if action == 'complete':
                drive.status = 'closed'

            elif action == 'reopen':
                drive.status = 'approved'
            else:
                return {'message': 'Valid action required: complete'}, 400

        else:
            return {'message': 'Access Denied!'}, 401

        db.session.commit()

        return {
            'message': 'Drive status updated!',
            'drive_id': drive.id,
            'status': drive.status
        }, 200
        

class ApplyDriveAPI(Resource):
    @jwt_required()
    def post(self, drive_id):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        
        if not current_user or current_user.role != 'student':
            return {"message": "Access Denied! Student only."}, 401
        
        # checking if drive exists and is approved
        drive = PlacementDrive.query.get(drive_id)
        if not drive:
            return {"message": "Drive not found!"}, 404
        if drive.status != 'approved':
            return {"message": "Cannot apply to non-approved drive!"}, 400
        
        student = current_user.student_profile 
        if not student:
            return {"message": "Student profile not complete!"}, 400
        
        # checking if already applied
        existing_app = Application.query.filter_by(
            student_id=student.id, 
            drive_id=drive_id
        ).first()
        if existing_app:
            return {"message": "Already applied to this drive!"}, 409
        
        # checking eligibility 
        if student.cgpa < drive.min_cgpa:
            return {"message": f"Minimum CGPA {drive.min_cgpa} required!"}, 400
        
        branches_list = drive.eligible_branches.split(',')
        if student.branch not in branches_list:
            return {"message": f"Eligible branches: {drive.eligible_branches}"}, 400
        
        if not student.resume:
            return {"message":"Upload resume in profile before applying!"},400

        new_app = Application(
            student_id=student.id,
            drive_id=drive_id,
            status='applied'
        )
        db.session.add(new_app)
        db.session.commit()
        
        return {
            "message": "Application submitted successfully!",
            "application_id": new_app.id,
            "status": new_app.status,
            "drive": drive.job_title
        }, 201


class CompanyDrivesAPI(Resource):

    @jwt_required()
    def get(self, company_user_id):

        company = Company.query.filter_by(user_id=company_user_id).first()
        description=company.description

        if not company:
            return {"message": "Company not found"}, 404

        drives = PlacementDrive.query.filter_by(
            company_id=company.id,
            status="approved"
        ).all()

        result = []

        for drive in drives:
            result.append({
                "drive_id": drive.id,
                "job_title": drive.job_title,
                "location": drive.location,
                "package": drive.salary,
                "deadline": drive.deadline.strftime("%Y-%m-%d") if drive.deadline else None
            })

        return {"drives": result, 'description':description}, 200