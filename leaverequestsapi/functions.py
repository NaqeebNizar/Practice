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


def add_leave_request(emp_id, leave_date, leave_reason, body, department):
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
        INSERT INTO leave_requests (emp_id, leave_date, leave_reason, email_body, department)
        VALUES (%s, %s, %s, %s, %s);
        """

        cur.execute(insert_query, (emp_id, leave_date, leave_reason, body, department))
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



def send_data_to_frontend(department_name):
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

        # Execute a query to retrieve pending leave requests for the specified department
        query = """
        SELECT lr.id, e.name, e.email, lr.leave_date, lr.leave_reason, lr.status, lr.email_body
        FROM leave_requests lr
        JOIN employees e ON lr.emp_id = e.emp_id
        JOIN departments d ON e.department = d.department_name
        WHERE d.department_name = %s AND lr.status = 'Pending'
        """
        cur.execute(query, (department_name,))
        
        # Fetch all results from the executed query
        rows = cur.fetchall()

        # Convert rows to a list of dictionaries
        columns = ['id', 'name', 'email', 'leave_date', 'leave_reason', 'status', 'email_body']
        data = [dict(zip(columns, row)) for row in rows]

        # Close cursor and connection
        cur.close()
        conn.close()

        return data

    except Exception as e:
        return False, str(e)
    




def update_employee_status(emp_id, leave_request_status):
    return emp_id,leave_request_status
    # try:
    #     # Establish connection to the PostgreSQL database
    #     conn = psycopg2.connect(
    #         host=os.getenv('DB_HOST'),
    #         user=os.getenv('DB_USER'),
    #         password=os.getenv('DB_PASSWORD'),
    #         dbname=os.getenv('DB_NAME'),
    #         port=os.getenv('DB_PORT')
    #     )
    #     cur = conn.cursor()

    #     # Execute a query to retrieve all leave requests
    #     query = "SELECT emp_id, leave_date, leave_reason, department FROM leave_requests;"
    #     cur.execute(query)
        
    #     # Fetch all results from the executed query
    #     rows = cur.fetchall()

    #     # Convert rows to a list of dictionaries
    #     columns = ['emp_id', 'leave_date', 'leave_reason', 'department']
    #     data = [dict(zip(columns, row)) for row in rows]

    #     # Close cursor and connection
    #     cur.close()
    #     conn.close()

    #     # Convert list of dictionaries to JSON
    #     json_data = json.dumps(data, default=str)

    #     data = json.loads(json_data)

    #     # Convert the Python object back to a formatted JSON string
    #     formatted_json_string = json.dumps(data, indent=4)

    #     return True, formatted_json_string

    # except Exception as e:
    #     return False, str(e)

