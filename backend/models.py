from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, Column, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime,date


#variable db
db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)                         # 'admin', 'company', 'student'
    is_active = db.Column(db.Boolean, default=True)
    status = db.Column(db.String(20), nullable=False, default='pending')

    student_profile = db.relationship('Student', backref='user', uselist=False, cascade="all, delete-orphan")
    company_profile = db.relationship('Company', backref='user', uselist=False, cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)
        if self.role == 'admin':
            self.status = 'approved'

class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(100))
    roll_number = db.Column(db.String(20), unique=True)
    branch = db.Column(db.String(50))
    cgpa = db.Column(db.Float)
    passout_year = db.Column(db.Integer)
    resume = db.Column(db.String(255))
    applications = db.relationship('Application', backref='student', lazy=True)


    
class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(120))
    hr_name = db.Column(db.String(20))
    hr_contact = db.Column(db.String(10))
    description = db.Column(db.String(200))    
    drives = db.relationship('PlacementDrive', backref='company', lazy=True)

class PlacementDrive(db.Model):
    __tablename__ = 'placement_drives'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.Text)

    eligible_branches = db.Column(db.String(255))                   # e.g., "CS,IT,ECE"
    min_cgpa = db.Column(db.Float, default=0.0)
    
    year_start = db.Column(db.Integer, nullable=False) 
    year_end = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')             # pending, approved, closed
    deadline = db.Column(db.DateTime)
    salary=db.Column(db.Integer)
    location=db.Column(db.String(64))
    
    applications = db.relationship('Application', backref='drive', lazy=True)

class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drives.id'), nullable=False)
    applied_on = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='applied')             # shortlisted, waiting, rejected  