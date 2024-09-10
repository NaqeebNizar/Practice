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

load_dotenv()

# connecting to database
def connect():
    try:
        # Establish connection to the PostgreSQL database
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            dbname=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT')
        )
        return conn

    except Exception as e:
        return False, str(e)


def get_smtp_settings():
    """
    Get the SMTP settings for sending emails using Zoho's SMTP server.
    """
    return ('smtp.zoho.com', 587, False)  # Zoho uses TLS on port 587


def add_leave_request(emp_id, leave_start_date, leave_end_date, leave_reason, department):
    try:
        # Ensure leave_start_date and leave_end_date are in date format
        if isinstance(leave_start_date, str):
            leave_start_date = datetime.strptime(leave_start_date, '%Y-%m-%d').date()
        if isinstance(leave_end_date, str):
            leave_end_date = datetime.strptime(leave_end_date, '%Y-%m-%d').date()

        # Establish connection to the PostgreSQL database
        conn = connect()

        if conn:
            cur = conn.cursor()

            # Initialize current_date with leave_start_date
            current_date = leave_start_date

            while current_date <= leave_end_date:
                # Insert a leave request for each date
                query = """
                INSERT INTO leave_requests (emp_id, department, leave_date, leave_reason, status)
                VALUES (%s, %s, %s, %s, %s)
                """
                cur.execute(query, (emp_id, department, current_date, leave_reason, "Pending"))
                
                # Move to the next day
                current_date += timedelta(days=1)

            # Commit the transaction
            conn.commit()

            # Close cursor and connection
            cur.close()
            conn.close()

            return True, "Leave request added successfully."
        else:
            return False, "Cannot connect to the database"

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


def send_updated_email(email_subject, approved_email_body, recipients, line_manager_email):
    """
    Send an email using SMTP.
    """
    message = MIMEMultipart()
    message['From'] = line_manager_email
    message['To'] = ", ".join(recipients)  
    message['Subject'] = email_subject
    
    message.attach(MIMEText(approved_email_body, 'html'))

    smtp_server, port, use_ssl = get_smtp_settings()
    
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(line_manager_email, "1234")
        server.sendmail(line_manager_email, recipients, message.as_string())
        server.quit()
        return True, "Email sent successfully to HR from line manager."
    except Exception as e:
        return False, f"Failed to send email: {str(e)}"




def send_data_to_frontend():
    try:
        # Establish connection to the PostgreSQL database
        conn = connect()
        cur = conn.cursor()

        if conn:
            # Query to retrieve leave requests
            query = """
            SELECT emp_id, leave_date, leave_reason, department, status, email_body 
            FROM leave_requests;
            """

            # Execute the query
            cur.execute(query)

            # Fetch all results from the executed query
            rows = cur.fetchall()

            # Convert rows to a list of dictionaries
            columns = ['emp_id', 'leave_date', 'leave_reason', 'department', 'status', 'email_body']
            data = [dict(zip(columns, row)) for row in rows]

            # Close cursor and connection
            cur.close()
            conn.close()

            return data

    except Exception as e:
        return False, str(e)
    



def send_filter_data_to_frontend(pin):
    try:
        # Establish connection to the PostgreSQL database
        conn = connect()

        if conn:
            cur = conn.cursor()

            # Define the query to find the department by pin
            query_department = "SELECT * FROM departments WHERE password = %s"
            cur.execute(query_department, (pin,))
            department = cur.fetchone()

            if department:
                department_name = department[0]  # Assuming department name is the second column
                
                # get the data from leave_requests table of specific department where status is pending
                # Define the query to find pending leave requests for the department
                query_leave_requests = """
                    SELECT * FROM leave_requests
                    WHERE department = %s AND status = 'Pending'
                """
                cur.execute(query_leave_requests, (department_name,))
                leave_requests = cur.fetchall()
                

                if leave_requests:
                    # Fetch the column names from the cursor
                    columns = [desc[0] for desc in cur.description]
                    
                    # Convert each row into a dictionary
                    leave_requests_dict = [
                        dict(zip(columns, row)) for row in leave_requests
                    ]

                    return leave_requests_dict
                else:
                    return "No Pending leave requests found with that department"
                
            else:
                # Close the cursor and connection
                cur.close()
                conn.close()
                return "No department found with the provided pin"

        else:
            return "cannot connect to database"
    except Exception as e:
        return str(e)
    
    



def check_pin_validation(pin):
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

        # Define the query to find the department by pin
        query_department = "SELECT * FROM departments WHERE password = %s"
        cur.execute(query_department, (pin,))
        department = cur.fetchone()

        if department:
            return True
            
        else:
            # Close the cursor and connection
            cur.close()
            conn.close()
            return False, "No department found with the provided pin"

    except Exception as e:
        return str(e)




def get_line_manager_email(department):
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

        # Query to retrieve line manager's email for the specified department
        query = """
        SELECT manager_email 
        FROM departments 
        WHERE department_name = %s;
        """
        
        # Execute the query
        cur.execute(query, (department,))

        # Fetch the result
        result = cur.fetchone()
        
        # Close cursor and connection
        cur.close()
        conn.close()

        if result:
            return result[0]  # Return the line manager email
        else:
            return None  # Return None if no match is found

    except Exception as e:
        return None, str(e)
    




def get_line_manager_email_and_password(department):
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            dbname=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT')
        )
        cur = conn.cursor()

        query = """
        SELECT manager_email, password
        FROM departments
        WHERE department_name = %s;
        """
        
        cur.execute(query, (department,))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result:
            return result[0], result[1]
        else:
            return None, None, "No department found with the specified name"

    except Exception as e:
        return None, None, str(e)

    









def update_leave_request_status(leave_request_id, employee_id, leave_status):
    try:
        # Establish connection to the PostgreSQL database
        conn = connect()

        if conn:
            cur = conn.cursor()

            # Query to get the current status of the leave request
            select_status_query = """
            SELECT status, department 
            FROM leave_requests 
            WHERE id = %s AND emp_id = %s;
            """
            cur.execute(select_status_query, (leave_request_id, employee_id))
            result = cur.fetchone()

            if result:
                current_status, department = result

                # Check if the current status is the same as the new status
                if current_status == leave_status:
                    # Close cursor and connection
                    cur.close()
                    conn.close()
                    return False, f"Leave request is already {current_status}"

                # Query to update the status of the leave request
                update_query = """
                UPDATE leave_requests 
                SET status = %s 
                WHERE id = %s AND emp_id = %s;
                """
                cur.execute(update_query, (leave_status, leave_request_id, employee_id))
                conn.commit()

                if cur.rowcount > 0:
                    # Close cursor and connection
                    cur.close()
                    conn.close()
                    return True, "Leave request status updated successfully"
                else:
                    # Close cursor and connection if no row was updated
                    cur.close()
                    conn.close()
                    return False, "No leave request found with the given ID and Employee ID"
            else:
                # Close cursor and connection if no department was found
                cur.close()
                conn.close()
                return False, "No leave request found with the given ID and Employee ID"

        else:
            return False, "Cannot connect to the database"

    except Exception as e:
        return False, str(e)



def get_employee_details(emp_id):
    try:
        # Establish connection to the PostgreSQL database
        conn = connect()

        if conn:
            cur = conn.cursor()

            # Query to get the employee's email and other details from the database based on emp_id
            select_query = """
            SELECT name, email, department 
            FROM employees 
            WHERE emp_id = %s;
            """
            cur.execute(select_query, (emp_id,))
            result = cur.fetchone()

            # If an employee is found, return the details
            if result:
                emp_name, emp_email, department = result
                cur.close()
                conn.close()

                return {
                    'name': emp_name,
                    'email': emp_email,
                    'department': department
                }

            # Close the cursor and connection if no employee is found
            cur.close()
            conn.close()
            return False

        else:
            return None  # If connection to the database fails

    except Exception as e:
        return None, str(e)


    














# current_date = start_date_obj
#             while current_date <= end_date_obj:
#                 # Insert a leave request for each date
#                 query = """
#                 INSERT INTO leave_requests (emp_id, department, leave_date, leave_reason, status)
#                 VALUES (%s, %s, %s, %s, %s)
#                 """
#                 cursor.execute(query, (emp_id, department, current_date, leave_reason, "Pending"))
                
#                 # Move to the next day
#                 current_date += timedelta(days=1)


# # Convert start_date and end_date to date objects
#         start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
#         end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()