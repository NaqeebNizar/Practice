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


from datetime import datetime, timedelta

def add_leave_request(emp_id, leave_start_date, leave_end_date, leave_duration, leave_reason, department):
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
            # Initialize current_date with leave_end_date to insert the last date first
            current_date = leave_end_date

            while current_date >= leave_start_date:
                # Insert a leave request for each date starting from the last date
                query = """
                INSERT INTO leave_requests (emp_id, department, leave_date, leave_reason, status, leave_duration)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cur.execute(query, (emp_id, department, current_date, leave_reason, "Pending", leave_duration))
                
                # Move to the previous day
                current_date -= timedelta(days=1)

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




def get_employee_details(emp_id):

    try:
        # Establish connection to the PostgreSQL database
        conn = connect()

        if conn:
            print("connection successfull")
            cur = conn.cursor()

            # SQL query to retrieve employee details by emp_id
            query = """
                SELECT * 
                FROM employees 
                WHERE emp_id = %s
            """

            # Execute the query and fetch the result
            cur.execute(query, (emp_id,))
            employee_details = cur.fetchall()

            # Close the cursor and connection
            cur.close()
            conn.close()

            # Return the employee details
            return employee_details

           
    except Exception as e:
        return str(e)




def send_data_to_frontend():
    try:
        print("In sebd_data function")
        # Establish connection to the PostgreSQL database
        conn = connect()
        cur = conn.cursor()

        if conn:
            # Query to retrieve leave requests and employee names
            print("Connection established")
            query = """
            SELECT lr.id, lr.emp_id, e.name AS emp_name, lr.leave_date, lr.leave_reason, lr.department, lr.status, lr.email_body, lr.leave_duration
            FROM leave_requests lr
            JOIN employees e ON lr.emp_id = e.emp_id
            ORDER BY 
                CASE 
                    WHEN lr.status = 'Approved' THEN 1
                    WHEN lr.status = 'Pending' THEN 2
                    WHEN lr.status = 'Declined' THEN 3
                    ELSE 4
                END;
            """

            # Execute the query
            cur.execute(query)
            print("Executed")
            # Fetch all results from the executed query
            rows = cur.fetchall()

            # Convert rows to a list of dictionaries
            columns = ['id', 'emp_id', 'emp_name', 'leave_date', 'leave_reason', 'department', 'status', 'email_body', 'leave_duration']
            data = [dict(zip(columns, row)) for row in rows]
            print(data)
            # Close cursor and connection
            cur.close()
            conn.close()

            return data

    except Exception as e:
        return False, str(e)



def send_filter_data_to_frontend(pin):
    print("func executed")
    try:
        # Establish connection to the PostgreSQL database
        conn = connect()

        if conn:
            print("connection successfull")
            cur = conn.cursor()

            # Define the query to find the department by pin
            query_department = "SELECT department_name FROM departments WHERE password = %s"
            cur.execute(query_department, (pin,))
            department = cur.fetchone()

            print("department matched")

            if department:
                print(department)
                department_name = department[0]


                print("leave request query executed")
                # Query to retrieve and filter leave requests for the specific department
                query_leave_requests = """
                SELECT lr.id, lr.emp_id, e.name AS emp_name, lr.leave_date, lr.leave_reason, lr.department, lr.status, lr.email_body, lr.leave_duration
                FROM leave_requests lr
                JOIN employees e ON lr.emp_id = e.emp_id
                WHERE lr.department = %s
                ORDER BY 
                    CASE 
                        WHEN lr.status = 'Pending' THEN 1
                        WHEN lr.status = 'Approved' THEN 2
                        WHEN lr.status = 'Declined' THEN 3
                        ELSE 4
                    END;
                """
                cur.execute(query_leave_requests, (department_name,))
                leave_requests = cur.fetchall()

                if not leave_requests:
                    return "No leave requests found for that department"


                print(leave_requests)
                # Convert rows to a list of dictionaries
                columns = ['id', 'emp_id', 'emp_name', 'leave_date', 'leave_reason', 'department', 'status', 'email_body', 'leave_duration']
                leave_requests = [dict(zip(columns, row)) for row in leave_requests]
                return leave_requests

            else:
                return "Department not found"

        else:
            return "Cannot connect to the database"
    except Exception as e:
        return str(e)



def send_email(subject, body, recipients, name ,sender_email, sender_password):
    """
    Send an email using SMTP.
    """
    print(f"email password = {sender_password}")
    message = MIMEMultipart()
    message['From'] = f"{name} <{sender_email}>"
    message['To'] = ", ".join(recipients)  # Join the recipients list into a single string
    message['Subject'] = subject
    
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





def employee_send_email(subject, body, recipients, name, sender_email, sender_password):
    """
    Send an email using SMTP.
    """
    print(f"{subject} {name} {sender_email} {body} {recipients} {sender_password} ")
    # message = MIMEMultipart()
    # message['From'] = f"{name} <{sender_email}>"
    # message['To'] = ", ".join(recipients)  # Join the recipients list into a single string
    # message['Subject'] = f"{subject}"
    
    # message.attach(MIMEText(body, 'html'))

    # smtp_server, port, use_ssl = get_smtp_settings()
    
    # try:
    #     server = smtplib.SMTP(smtp_server, port)
    #     server.starttls()
    #     server.login(sender_email, sender_password)
    #     server.sendmail(sender_email, recipients, message.as_string())  # Pass the list of recipients
    #     server.quit()
    #     return True, "Email sent successfully."
    # except Exception as e:
    #     return False, f"Failed to send email: {str(e)}"

    



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

        # Query to retrieve the line manager's email and name for the specified department
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
            # Return both the manager's email and name
            manager_email = result
            return manager_email
        else:
            return None, None  # Return None if no match is found

    except Exception as e:
        return None, str(e)





def update_leave_request_status(leave_request_id, employee_id, leave_status):
    try:
        # Establish connection to the PostgreSQL database
        conn = connect()

        if conn:
            cur = conn.cursor()

            # Query to get the current status of the leave request
            select_status_query = """
            SELECT status 
            FROM leave_requests 
            WHERE id = %s AND emp_id = %s;
            """
            cur.execute(select_status_query, (leave_request_id, employee_id))
            result = cur.fetchone()

            if result:
                current_status = result[0]

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
                    return "Leave request status updated successfully"
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




def get_employee_email(emp_id):
    try:
        # Establish connection to the PostgreSQL database
        conn = connect()

        if conn:
            cur = conn.cursor()

            # Define the query to retrieve the employee email based on emp_id
            query = "SELECT email FROM employees WHERE emp_id = %s"
            cur.execute(query, (emp_id,))

            # Fetch the employee email
            employee_email = cur.fetchone()

            cur.close()
            conn.close()

            if employee_email:
                # Return the email if found
                return employee_email[0]
            else:
                return None  # No employee found with the given emp_id

        else:
            return None  # If connection to the database fails

    except Exception as e:
        return None, str(e)



def calculate_leave_tracking(emp_id, leave_duration, leave_type):
    try:
        # Establish connection to the PostgreSQL database
        conn = connect()

        if conn:
            cur = conn.cursor()

            # Retrieve current leave data for the given emp_id
            cur.execute("""
                SELECT total_annual, annual_consumed, total_sick, sick_consumed, total_casual, casual_consumed
                FROM leave_tracking
                WHERE emp_id = %s
            """, (emp_id,))
            record = cur.fetchone()

            if record:
                # Convert fetched data to integers (handling possible conversion issues)
                total_annual = int(record[0]) if record[0] else 0
                annual_consumed = int(record[1]) if record[1] else 0
                total_sick = int(record[2]) if record[2] else 0
                sick_consumed = int(record[3]) if record[3] else 0
                total_casual = int(record[4]) if record[4] else 0
                casual_consumed = int(record[5]) if record[5] else 0

                # Calculate consumed fields based on leave_type
                if leave_type == 'annualleave':
                    annual_consumed += int(leave_duration)
                elif leave_type == 'sickleave':
                    sick_consumed += int(leave_duration)
                elif leave_type == 'casualleave':
                    casual_consumed += int(leave_duration)
                else:
                    # Handle other leave types if needed
                    pass

                # Update the leave_tracking table with the new values
                cur.execute("""
                    UPDATE leave_tracking
                    SET annual_consumed = %s,
                        sick_consumed = %s,
                        casual_consumed = %s
                    WHERE emp_id = %s
                """, (annual_consumed, sick_consumed, casual_consumed, emp_id))

                # Commit the changes
                conn.commit()

                cur.close()
                conn.close()
                return True, "Leave tracking updated successfully and email sent successfully."

            else:
                cur.close()
                conn.close()
                return None, "No employee leave tracking found for the given emp_id."

        else:
            return None, "Failed to connect to the database."

    except Exception as e:
        return None, str(e)