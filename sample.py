# var = "casual"

# print(var.upper())
# print(var.lower())
# print(var.capitalize())





from datetime import timedelta, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
# from django.db import IntegrityError
# from .models import LeaveRequest
import psycopg2
import os
from dotenv import load_dotenv
import json
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.response import Response



def get_smtp_settings():
    """
    Get the SMTP settings for sending emails using Zoho's SMTP server.
    """
    return ('smtp.zoho.com', 587, False)  # Zoho uses TLS on port 587

def send_email(subject, body, recipients, sender_name, HR_name, employee_name,sender_email, sender_password, status):
    """
    Send an email using SMTP.
    """
    print(f"email password = {sender_password}")
    print(status)

    if status == "Approved":
        message = MIMEMultipart()
        message['From'] = f"{sender_name.capitalize()} <{sender_email}>"
        message['To'] = f"{HR_name} {recipients}"
        message['Subject'] = f"{subject.capitalize()} for {employee_name.capitalize()} has been {status}"
        
        message.attach(MIMEText(body, 'html'))

        smtp_server, port, use_ssl = get_smtp_settings()
        
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, message.as_string())  # Pass the list of recipients
            server.quit()
            return True, "Email sent successfully."
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"
        

    elif status == "Declined":
        message = MIMEMultipart()
        message['From'] = f"{sender_name.capitalize()} <{sender_email}>"
        message['To'] = f"{employee_name} {recipients}"
        message['Subject'] = f"{employee_name.capitalize()} your leave request for {subject.capitalize()} has been {status}"
        
        message.attach(MIMEText(body, 'html'))

        smtp_server, port, use_ssl = get_smtp_settings()
        
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipients, message.as_string())  # Pass the list of recipients
            server.quit()
            return True, "Email sent successfully."
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"
        
    
    


recipient1 = "de.naqeeb@brbgroup.pk"

send_email("email_subject", "declined_email_body", recipient1, "lineManager","HR", "employeeName","de.naqeeb@brbgroup.pk", "DeNaqeeb@321","Approved")


# if declined hai
recipient2 = "de.naqeeb@brbgroup.pk"

send_email("email_subject", "declined_email_body", recipient1, "lineManager","HR", "employeeName","de.naqeeb@brbgroup.pk", "DeNaqeeb@321","Declined")
