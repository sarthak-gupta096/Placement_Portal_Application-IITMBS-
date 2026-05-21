from worker import celery_app
from celery.schedules import crontab
from models import Users
from jinja2 import Template
from datetime import datetime, timedelta
from sqlalchemy import func
from models import db, PlacementDrive, Application
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import csv
import os
from email.mime.base import MIMEBase 
from email import encoders           



def send_mail(email, subject, email_content, attachement=None):
    smtp_server_host = "localhost"
    smtp_port = 1025 
    sender_email = "admin@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg["Subject"] = subject


    msg.attach(MIMEText(email_content, "html"))

    # Attachment logic
    if attachement and os.path.exists(attachement):
        with open(attachement, "rb") as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
        
            part.add_header(
                'Content-Disposition', 
                f'attachment; filename="{os.path.basename(attachement)}"'
            )
            msg.attach(part)

    try:
        
        server = smtplib.SMTP(host=smtp_server_host, port=smtp_port)
    
        server.send_message(msg)
        server.quit()
        print(f"Mail sent to {email}!")
    except Exception as e:
        print(f"Error sending mail: {e}")




def get_html_report(counts_list):
    with open("report.html", "r") as file:
        jinja_template = Template(file.read())
        return jinja_template.render(counts=counts_list, sender_name="Placement Coordinator")


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):    
    sender.add_periodic_task(10.0, monthly_report.s(), name='report at every 10s for test')

    # 1st day of every month
    sender.add_periodic_task(
    crontab(hour=7, minute=0, day_of_month=1),
    monthly_report.s(),
    name='monthly_report on 1st day of every month'
)
    sender.add_periodic_task(10.0, daily_remainder.s(), name='daily_remainder')
    sender.add_periodic_task(
    crontab(hour=9, minute=0),
    daily_remainder.s(),
    name='daily_reminder at 9 AM'
)

   

@celery_app.task
def test(arg):
    print(arg)



@celery_app.task
def daily_remainder():
    today=datetime.utcnow()
    tomorrow = datetime.utcnow() + timedelta(days=1)
    drives = PlacementDrive.query.filter(
        PlacementDrive.deadline >= today,
        PlacementDrive.deadline <= tomorrow,
        PlacementDrive.status == "approved"
    ).all()

    students = Users.query.filter_by(role='student', status='approved').all()

    for drive in drives:
        for student_user in students:

            student = student_user.student_profile
            if not student:
                continue

            branches = drive.eligible_branches.split(",")

            if student.branch in branches and student.cgpa >= drive.min_cgpa:

                msg = f"""
                <h3>Placement Drive Reminder</h3>

                Company: {drive.company.name}<br>
                Job Role: {drive.job_title}<br>
                Deadline: {drive.deadline.strftime('%Y-%m-%d')}<br>

                Apply before deadline.
                """

                send_mail(
                    email=student_user.email,
                    subject="Placement Drive Deadline Reminder",
                    email_content=msg
                )

    print("Daily reminders sent!")


@celery_app.task
def monthly_report():
    total_drives = PlacementDrive.query.filter(PlacementDrive.status.in_(['approved', 'closed'])).count()
    total_applied = db.session.query(Application.student_id).distinct().count()
    total_selected = Application.query.filter_by(status='shortlisted').count()

    report_data = [
        f"Total Number of Drives Conducted: {total_drives}",
        f"Total Number of Students Applied: {total_applied}",
        f"Total Number of Students Selected: {total_selected}"
    ]

    html_report = get_html_report(report_data)
    
    send_mail(email="admin@gmail.com", subject="Monthly Placement Report", email_content=html_report)


@celery_app.task
def data_export(placement_history, student_email): 
    with open('data_export.csv', 'w', newline='') as csvfile:
        fieldnames = [
            "student_id",
            "company_name",
            "job_title",
            "status",
            "applied_on"
            ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
    
        writer.writerows(placement_history) 

    send_mail(email=student_email, email_content="Please find your exported placement history attached.", subject="Placement History Export",
               attachement="data_export.csv")    
    return 'Data exported!'