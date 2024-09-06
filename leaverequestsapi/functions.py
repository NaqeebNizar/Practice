from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
# from django.db import IntegrityError
# from .models import LeaveRequest
import psycopg2
import os
from dotenv import load_dotenv
import json


load_dotenv()


def get_smtp_settings():
    """
    Get the SMTP settings for sending emails using Zoho's SMTP server.
    """
    return ('smtp.zoho.com', 587, False)  # Zoho uses TLS on port 587


def add_leave_request(emp_id, leave_date, leave_reason, department):
    try:
        # Establish connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            dbname=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT')
        )
        cur = conn.cursor()

        # Insert the leave request into the 'leave_requests' table (assuming table structure)
        insert_query = """
        INSERT INTO leave_requests (emp_id, leave_date, leave_reason, department)
        VALUES (%s, %s, %s, %s);
        """

        cur.execute(insert_query, (emp_id, leave_date, leave_reason, department))
        # Commit the transaction
        conn.commit()


        # Close cursor and connection
        cur.close()
        conn.close()

        return True, "Leave request added successfully."

    except Exception as e:
        return False, str(e)


def send_email(subject, body, recipients, sender_email, sender_password):
    """
    Send an email using SMTP.
    """
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = ", ".join(recipients)  
    message['Subject'] = subject
    
    message.attach(MIMEText(body, 'html'))

    smtp_server, port, use_ssl = get_smtp_settings()
    
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipients, message.as_string())
        server.quit()
        return True, "Email sent successfully."
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"



def send_data_to_frontend():
    try:
        # Establish connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            dbname=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT')
        )
        cur = conn.cursor()

        # Execute a query to retrieve all leave requests
        query = "SELECT emp_id, leave_date, leave_reason, department FROM leave_requests;"
        cur.execute(query)
        
        # Fetch all results from the executed query
        rows = cur.fetchall()

        # Convert rows to a list of dictionaries
        columns = ['emp_id', 'leave_date', 'leave_reason', 'department']
        data = [dict(zip(columns, row)) for row in rows]

        # Close cursor and connection
        cur.close()
        conn.close()

        # Convert list of dictionaries to JSON
        json_data = json.dumps(data, default=str)

        data = json.loads(json_data)

        # Convert the Python object back to a formatted JSON string
        formatted_json_string = json.dumps(data, indent=4)

        return True, formatted_json_string

    except Exception as e:
        return False, str(e)