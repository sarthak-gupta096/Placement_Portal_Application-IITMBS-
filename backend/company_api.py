from flask import request, current_app as app
from flask_restful import Resource, Api
from models import db, Users, Company, Student, PlacementDrive
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required




class CompanyDashboardAPI(Resource):
    @jwt_required()
    def get(self):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        
        if not current_user or current_user.role != 'company':
            return {"message": "Access Denied!"}, 401
        
        current_company = current_user.company_profile
        if not current_company:
            return {"message": "Company profile not found!"}, 404
        
        # Using relationship: company.drives gives all drives with applicant count
        drives = []
        for drive in current_company.drives:  # Relationship from Company model
            drives.append({
                "drive_id": drive.id,
                "job_title": drive.job_title,
                "deadline": drive.deadline.strftime("%Y-%m-%d"),
                "applicants_count": len(drive.applications),  # Magic! Relationship count
                "status": drive.status
            })
        
        return {
            "company": {
                "id": current_company.id,
                "name": current_company.name,
                "description": current_company.description,
                "website": current_company.website,
                "hr_name": current_company.hr_name,
                "hr_contact": current_company.hr_contact
            },
            "drives": drives,
            "total_drives": len(drives),
            "total_applicants": sum(len(drive.applications) for drive in current_company.drives)
        }, 200


class CompanyAPI(Resource):
    @jwt_required()
    def get(self):
        search = request.args.get("search")
        query = Users.query.filter_by(role='company', status='approved')

        if search:
            query = query.join(Company).filter(
                Company.name.ilike(f"%{search}%"))

        companies = query.all()
        result=[]
        for user in companies:
            company_dict={
            "user_id": user.id,
            "name": user.company_profile.name if user.company_profile else None,
            "website": user.company_profile.website if user.company_profile else None,
            "hr_name": user.company_profile.hr_name if user.company_profile else None,
            "hr_contact": user.company_profile.hr_contact if user.company_profile else None,
            'status':user.status if user.status else None,
            'is_active':user.is_active
        }
            result.append(company_dict)
        return {
            "message": "Registered Companies",
            'registered-companies': result
        }, 200
        
    
    @jwt_required()
    def put(self, user_id):
        id_from_token = get_jwt_identity()

        if str(id_from_token) != str(user_id):
             return {"message": "Access Denied!"}, 401

        user = Users.query.get(user_id)
        if not user or not user.company_profile:
            return {'message': 'Company not found!'}, 404
        
        data = request.json
        user.email = data.get('email', user.email)
        if data.get('password'):
            user.password = data.get('password')
        
        comp = user.company_profile
        comp.name = data.get('name', comp.name)
        comp.website = data.get('website', comp.website)
        comp.hr_name = data.get('hr_name', comp.hr_name)
        comp.hr_contact = data.get('hr_contact', comp.hr_contact)

        db.session.commit()
        return {"message": "Profile Updated Successfully!"}, 200
    
    @jwt_required()
    def delete(self, user_id):
        current_user = Users.query.get(get_jwt_identity())
        if current_user.role != 'admin':
            return {"message": "Access Denied!"}, 401

        user = Users.query.get(user_id)
        if not user:
            return {'message': 'Company not found!'}, 404

        db.session.delete(user)                                    # Cascade deletes profile
        db.session.commit()
        return {"message": "Company Profile Deleted Successfully!"}, 200
    
    @jwt_required()
    def patch(self,user_id):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        if not current_user or current_user.role !='admin':
            return {"message":"Access Denied!"},401
        
        current_comp=Users.query.get(user_id)
        if current_comp:
            current_comp.status='approved'
            db.session.commit()
            return {"message":"Company Approved Successfully!"}
    
class SearchCompaniesAPI(Resource):

    @jwt_required()
    def get(self):

        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)

        if not current_user or current_user.role != "admin":
            return {"message": "Access Denied! Admin only."}, 401

        search = request.args.get("search")

        query = Users.query.filter_by(role='company', status='approved')

        if search:
            query = query.join(Company).filter(
                Company.name.ilike(f"%{search}%")
            )

        companies = query.all()

        result = []

        for user in companies:
            result.append({
                "user_id": user.id,
                "name": user.company_profile.name if user.company_profile else None,
                "website": user.company_profile.website if user.company_profile else None,
                "hr_name": user.company_profile.hr_name if user.company_profile else None,
                "hr_contact": user.company_profile.hr_contact if user.company_profile else None,
                "status": user.status,
                "is_active": user.is_active
            })

        return {
            "message": "Companies Search Result",
            "companies": result
        }, 200

class CompProfileAPI(Resource):
    @jwt_required()
    def patch(self,user_id):
        id_from_token = get_jwt_identity()
        current_user = Users.query.get(id_from_token)
        if not current_user or current_user.role !='admin':
            return {"message":"Access Denied!"},401
        
        current_comp=Users.query.get(user_id)

        data = request.get_json()
        action = data.get('action')
        if action == 'active':
            current_comp.is_active = True
            db.session.commit()
            return {"message":"Company Reactivated Successfully!"}
        
        elif action == 'blacklist':
            current_comp.is_active = False
            db.session.commit()
            return {"message":"Company Blacklisted Successfully!"}