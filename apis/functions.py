# from datetime import timedelta, datetime
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import smtplib
# # from django.db import IntegrityError
# # from .models import LeaveRequest
# import psycopg2
# import os
# from dotenv import load_dotenv
# import json
# from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
# from rest_framework.response import Response

# load_dotenv()

# # connecting to database
# def connect():
#     try:
#         # Establish connection to the PostgreSQL database
#         conn = psycopg2.connect(
#             host=os.getenv('DB_HOST'),
#             user=os.getenv('DB_USER'),
#             password=os.getenv('DB_PASSWORD'),
#             dbname=os.getenv('DB_NAME'),
#             port=os.getenv('DB_PORT')
#         )
#         return conn

#     except Exception as e:
#         return False, str(e)


# def get_smtp_settings():
#     """
#     Get the SMTP settings for sending emails using Zoho's SMTP server.
#     """
#     return ('smtp.zoho.com', 587, False)  # Zoho uses TLS on port 587


# from datetime import datetime, timedelta

# def add_leave_request(emp_id, leave_start_date, leave_end_date, leave_duration, leave_reason, department):
#     try:
#         # Ensure leave_start_date and leave_end_date are in date format
#         if isinstance(leave_start_date, str):
#             leave_start_date = datetime.strptime(leave_start_date, '%Y-%m-%d').date()
#         if isinstance(leave_end_date, str):
#             leave_end_date = datetime.strptime(leave_end_date, '%Y-%m-%d').date()

#         # Establish connection to the PostgreSQL database
#         conn = connect()

#         if conn:
#             cur = conn.cursor()
#             # Initialize current_date with leave_end_date to insert the last date first
#             current_date = leave_end_date

#             while current_date >= leave_start_date:
#                 # Insert a leave request for each date starting from the last date
#                 query = """
#                 INSERT INTO leave_requests (emp_id, department, leave_date, leave_reason, status, leave_duration)
#                 VALUES (%s, %s, %s, %s, %s, %s)
#                 """
#                 cur.execute(query, (emp_id, department, current_date, leave_reason, "Pending", leave_duration))
                
#                 # Move to the previous day
#                 current_date -= timedelta(days=1)

#             # Commit the transaction
#             conn.commit()

#             # Close cursor and connection
#             cur.close()
#             conn.close()

#             return True, "Leave request added successfully."
#         else:
#             return False, "Cannot connect to the database"

#     except Exception as e:
#         return False, str(e)




# def get_employee_details(emp_id):

#     try:
#         # Establish connection to the PostgreSQL database
#         conn = connect()

#         if conn:
#             print("connection successfull")
#             cur = conn.cursor()

#             # SQL query to retrieve employee details by emp_id
#             query = """
#                 SELECT * 
#                 FROM employees 
#                 WHERE emp_id = %s
#             """

#             # Execute the query and fetch the result
#             cur.execute(query, (emp_id,))
#             employee_details = cur.fetchall()

#             # Close the cursor and connection
#             cur.close()
#             conn.close()

#             # Return the employee details
#             return employee_details

           
#     except Exception as e:
#         return str(e)




# def send_data_to_frontend():
#     try:
#         print("In sebd_data function")
#         # Establish connection to the PostgreSQL database
#         conn = connect()
#         cur = conn.cursor()

#         if conn:
#             # Query to retrieve leave requests and employee names
#             print("Connection established")
#             query = """
#             SELECT lr.id, lr.emp_id, e.name AS emp_name, lr.leave_date, lr.leave_reason, lr.department, lr.status, lr.email_body, lr.leave_duration
#             FROM leave_requests lr
#             JOIN employees e ON lr.emp_id = e.emp_id
#             ORDER BY 
#                 CASE 
#                     WHEN lr.status = 'Approved' THEN 1
#                     WHEN lr.status = 'Pending' THEN 2
#                     WHEN lr.status = 'Declined' THEN 3
#                     ELSE 4
#                 END;
#             """

#             # Execute the query
#             cur.execute(query)
#             print("Executed")
#             # Fetch all results from the executed query
#             rows = cur.fetchall()

#             # Convert rows to a list of dictionaries
#             columns = ['id', 'emp_id', 'emp_name', 'leave_date', 'leave_reason', 'department', 'status', 'email_body', 'leave_duration']
#             data = [dict(zip(columns, row)) for row in rows]
#             print(data)
#             # Close cursor and connection
#             cur.close()
#             conn.close()

#             return data

#     except Exception as e:
#         return False, str(e)



# def send_filter_data_to_frontend(pin):
#     print("func executed")
#     try:
#         # Establish connection to the PostgreSQL database
#         conn = connect()

#         if conn:
#             print("connection successfull")
#             cur = conn.cursor()

#             # Define the query to find the department by pin
#             query_department = "SELECT department_name FROM departments WHERE password = %s"
#             cur.execute(query_department, (pin,))
#             department = cur.fetchone()

#             print("department matched")

#             if department:
#                 print(department)
#                 department_name = department[0]


#                 print("leave request query executed")
#                 # Query to retrieve and filter leave requests for the specific department
#                 query_leave_requests = """
#                 SELECT lr.id, lr.emp_id, e.name AS emp_name, lr.leave_date, lr.leave_reason, lr.department, lr.status, lr.email_body, lr.leave_duration
#                 FROM leave_requests lr
#                 JOIN employees e ON lr.emp_id = e.emp_id
#                 WHERE lr.department = %s
#                 ORDER BY 
#                     CASE 
#                         WHEN lr.status = 'Pending' THEN 1
#                         WHEN lr.status = 'Approved' THEN 2
#                         WHEN lr.status = 'Declined' THEN 3
#                         ELSE 4
#                     END;
#                 """
#                 cur.execute(query_leave_requests, (department_name,))
#                 leave_requests = cur.fetchall()

#                 if not leave_requests:
#                     return "No leave requests found for that department"


#                 print(leave_requests)
#                 # Convert rows to a list of dictionaries
#                 columns = ['id', 'emp_id', 'emp_name', 'leave_date', 'leave_reason', 'department', 'status', 'email_body', 'leave_duration']
#                 leave_requests = [dict(zip(columns, row)) for row in leave_requests]
#                 return leave_requests

#             else:
#                 return "Department not found"

#         else:
#             return "Cannot connect to the database"
#     except Exception as e:
#         return str(e)



# def send_email(subject, body, recipients, name ,sender_email, sender_password):
#     """
#     Send an email using SMTP.
#     """
#     print(f"email password = {sender_password}")
#     message = MIMEMultipart()
#     message['From'] = f"{name} <{sender_email}>"
#     message['To'] = ", ".join(recipients)  # Join the recipients list into a single string
#     message['Subject'] = subject
    
#     message.attach(MIMEText(body, 'html'))

#     smtp_server, port, use_ssl = get_smtp_settings()
    
#     try:
#         server = smtplib.SMTP(smtp_server, port)
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.sendmail(sender_email, recipients, message.as_string())  # Pass the list of recipients
#         server.quit()
#         return True, "Email sent successfully."
#     except Exception as e:
#         return False, f"Failed to send email: {str(e)}"





# def employee_send_email(subject, body, recipients, name, sender_email, sender_password):
#     """
#     Send an email using SMTP.
#     """
#     print(f"email password = {sender_password}")
#     message = MIMEMultipart()
#     message['From'] = f"{name} <{sender_email}>"
#     message['To'] = ", ".join(recipients)  # Join the recipients list into a single string
#     message['Subject'] = subject
    
#     message.attach(MIMEText(body, 'html'))

#     smtp_server, port, use_ssl = get_smtp_settings()
    
#     try:
#         server = smtplib.SMTP(smtp_server, port)
#         server.starttls()
#         server.login(sender_email, sender_password)
#         server.sendmail(sender_email, recipients, message.as_string())  # Pass the list of recipients
#         server.quit()
#         return True, "Email sent successfully."
#     except Exception as e:
#         return False, f"Failed to send email: {str(e)}"

    



# def check_pin_validation(pin):
#     try:
#         # Establish connection to the PostgreSQL database
#         conn = psycopg2.connect(
#             host=os.getenv('DB_HOST'),
#             user=os.getenv('DB_USER'),
#             password=os.getenv('DB_PASSWORD'),
#             dbname=os.getenv('DB_NAME'),
#             port=os.getenv('DB_PORT')
#         )
#         cur = conn.cursor()

#         # Define the query to find the department by pin
#         query_department = "SELECT * FROM departments WHERE password = %s"
#         cur.execute(query_department, (pin,))
#         department = cur.fetchone()

#         if department:
#             return True
            
#         else:
#             # Close the cursor and connection
#             cur.close()
#             conn.close()
#             return False, "No department found with the provided pin"

#     except Exception as e:
#         return str(e)




# def get_line_manager_email(department):
#     try:
#         # Establish connection to the PostgreSQL database
#         conn = psycopg2.connect(
#             host=os.getenv('DB_HOST'),
#             user=os.getenv('DB_USER'),
#             password=os.getenv('DB_PASSWORD'),
#             dbname=os.getenv('DB_NAME'),
#             port=os.getenv('DB_PORT')
#         )
#         cur = conn.cursor()

#         # Query to retrieve the line manager's email and name for the specified department
#         query = """
#         SELECT manager_email
#         FROM departments 
#         WHERE department_name = %s;
#         """
        
#         # Execute the query
#         cur.execute(query, (department,))

#         # Fetch the result
#         result = cur.fetchone()
        
#         # Close cursor and connection
#         cur.close()
#         conn.close()

#         if result:
#             # Return both the manager's email and name
#             manager_email = result
#             return manager_email
#         else:
#             return None, None  # Return None if no match is found

#     except Exception as e:
#         return None, str(e)





# def update_leave_request_status(leave_request_id, employee_id, leave_status):
#     try:
#         # Establish connection to the PostgreSQL database
#         conn = connect()

#         if conn:
#             cur = conn.cursor()

#             # Query to get the current status of the leave request
#             select_status_query = """
#             SELECT status 
#             FROM leave_requests 
#             WHERE id = %s AND emp_id = %s;
#             """
#             cur.execute(select_status_query, (leave_request_id, employee_id))
#             result = cur.fetchone()

#             if result:
#                 current_status = result[0]

#                 # Check if the current status is the same as the new status
#                 if current_status == leave_status:
#                     # Close cursor and connection
#                     cur.close()
#                     conn.close()
#                     return False, f"Leave request is already {current_status}"

#                 # Query to update the status of the leave request
#                 update_query = """
#                 UPDATE leave_requests 
#                 SET status = %s 
#                 WHERE id = %s AND emp_id = %s;
#                 """
#                 cur.execute(update_query, (leave_status, leave_request_id, employee_id))
#                 conn.commit()

#                 if cur.rowcount > 0:
#                     # Close cursor and connection
#                     cur.close()
#                     conn.close()
#                     return "Leave request status updated successfully"
#                 else:
#                     # Close cursor and connection if no row was updated
#                     cur.close()
#                     conn.close()
#                     return False, "No leave request found with the given ID and Employee ID"
#             else:
#                 # Close cursor and connection if no department was found
#                 cur.close()
#                 conn.close()
#                 return False, "No leave request found with the given ID and Employee ID"

#         else:
#             return False, "Cannot connect to the database"

#     except Exception as e:
#         return False, str(e)



# def get_employee_details(emp_id):
#     try:
#         # Establish connection to the PostgreSQL database
#         conn = connect()

#         if conn:
#             cur = conn.cursor()

#             # Query to get the employee's email and other details from the database based on emp_id
#             select_query = """
#             SELECT name, email, department 
#             FROM employees
#             WHERE emp_id = %s;
#             """
#             cur.execute(select_query, (emp_id,))
#             result = cur.fetchone()

#             # If an employee is found, return the details
#             if result:
#                 emp_name, emp_email, department = result
#                 cur.close()
#                 conn.close()

#                 return {
#                     'name': emp_name,
#                     'email': emp_email,
#                     'department': department
#                 }

#             # Close the cursor and connection if no employee is found
#             cur.close()
#             conn.close()
#             return False

#         else:
#             return None  # If connection to the database fails

#     except Exception as e:
#         return None, str(e)




# def get_employee_email(emp_id):
#     try:
#         # Establish connection to the PostgreSQL database
#         conn = connect()

#         if conn:
#             cur = conn.cursor()

#             # Define the query to retrieve the employee email based on emp_id
#             query = "SELECT email FROM employees WHERE emp_id = %s"
#             cur.execute(query, (emp_id,))

#             # Fetch the employee email
#             employee_email = cur.fetchone()

#             cur.close()
#             conn.close()

#             if employee_email:
#                 # Return the email if found
#                 return employee_email[0]
#             else:
#                 return None  # No employee found with the given emp_id

#         else:
#             return None  # If connection to the database fails

#     except Exception as e:
#         return None, str(e)



# def calculate_leave_tracking(emp_id, leave_duration, leave_type):
#     try:
#         # Establish connection to the PostgreSQL database
#         conn = connect()

#         if conn:
#             cur = conn.cursor()

#             # Retrieve current leave data for the given emp_id
#             cur.execute("""
#                 SELECT total_annual, annual_consumed, total_sick, sick_consumed, total_casual, casual_consumed
#                 FROM leave_tracking
#                 WHERE emp_id = %s
#             """, (emp_id,))
#             record = cur.fetchone()

#             if record:
#                 # Convert fetched data to integers (handling possible conversion issues)
#                 total_annual = int(record[0]) if record[0] else 0
#                 annual_consumed = int(record[1]) if record[1] else 0
#                 total_sick = int(record[2]) if record[2] else 0
#                 sick_consumed = int(record[3]) if record[3] else 0
#                 total_casual = int(record[4]) if record[4] else 0
#                 casual_consumed = int(record[5]) if record[5] else 0

#                 # Calculate consumed fields based on leave_type
#                 if leave_type == 'annualleave':
#                     annual_consumed += int(leave_duration)
#                 elif leave_type == 'sickleave':
#                     sick_consumed += int(leave_duration)
#                 elif leave_type == 'casualleave':
#                     casual_consumed += int(leave_duration)
#                 else:
#                     # Handle other leave types if needed
#                     pass

#                 # Update the leave_tracking table with the new values
#                 cur.execute("""
#                     UPDATE leave_tracking
#                     SET annual_consumed = %s,
#                         sick_consumed = %s,
#                         casual_consumed = %s
#                     WHERE emp_id = %s
#                 """, (annual_consumed, sick_consumed, casual_consumed, emp_id))

#                 # Commit the changes
#                 conn.commit()

#                 cur.close()
#                 conn.close()
#                 return True, "Leave tracking updated successfully and email sent successfully."

#             else:
#                 cur.close()
#                 conn.close()
#                 return None, "No employee leave tracking found for the given emp_id."

#         else:
#             return None, "Failed to connect to the database."

#     except Exception as e:
#         return None, str(e)











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





# def employee_send_email(subject, body, recipients, name, sender_email, sender_password):
#     """
#     Send an email using SMTP.
#     """
#     print(f"{subject} {name} {sender_email} {body} {recipients} {sender_password} ")
#     # message = MIMEMultipart()
#     # message['From'] = f"{name} <{sender_email}>"
#     # message['To'] = ", ".join(recipients)  # Join the recipients list into a single string
#     # message['Subject'] = f"{subject}"
    
#     # message.attach(MIMEText(body, 'html'))

#     # smtp_server, port, use_ssl = get_smtp_settings()
    
#     # try:
#     #     server = smtplib.SMTP(smtp_server, port)
#     #     server.starttls()
#     #     server.login(sender_email, sender_password)
#     #     server.sendmail(sender_email, recipients, message.as_string())  # Pass the list of recipients
#     #     server.quit()
#     #     return True, "Email sent successfully."
#     # except Exception as e:
#     #     return False, f"Failed to send email: {str(e)}"

    



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
            query = "SELECT name, email FROM employees WHERE emp_id = %s"
            cur.execute(query, (emp_id,))

            # Fetch the employee email
            employee = cur.fetchall()

            cur.close()
            conn.close()

            if employee:
                # Return the email if found
                return employee
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
    



def get_line_manager_name(department_name):
    """
    Retrieve the line manager's name for the provided department.
    """
    try:
        # Establish connection to the PostgreSQL database
        conn = connect()

        if conn:
            cur = conn.cursor()

            # Query to get the line manager's name based on department
            query = """
            SELECT manager_name
            FROM departments
            WHERE department_name = %s
            LIMIT 1;
            """
            
            cur.execute(query, (department_name,))  # Avoid SQL injection by using parameterized queries
            result = cur.fetchone()

            # Close the cursor and connection
            cur.close()
            conn.close()

            # Check if a result was found
            if result:
                return result[0], None  # Return the line manager's name
            else:
                return None, "No line manager found for the specified department."

    except Exception as e:
        return None, str(e)








from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
import time
import os




def get_edge_options(headless=True):
    edge_options = EdgeOptions()
    edge_options.binary_location = '/usr/bin/microsoft-edge'  # Path to the Edge binary
    edge_options.add_argument(r"user-data-dir=/home/brb/.config/microsoft-edge/Profile\ 2")  # Path to user data
    edge_options.add_argument("--profile-directory=Profile 2")

    if headless:
        edge_options.add_argument("--headless=new")
        edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--window-size=1920,1080")
        edge_options.add_argument("--start-maximized")
        edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36")
    
    edge_service = EdgeService(executable_path='/usr/local/bin/msedgedriver')
    
    driver = webdriver.Edge(service=edge_service, options=edge_options)
    return driver

# def get_edge_options(headless=True):
#     edge_options = Options()
#     edge_options.binary_location = '/usr/bin/microsoft-edge'  # Path to the Edge binary
#     edge_options.add_argument(r"user-data-dir=/home/brb/.config/microsoft-edge/Profile 1")  # Path to user data
#     edge_options.add_argument("--profile-directory=Profile 1")

#     if headless:
#         print('here')
#         print('==============================================================')

#         edge_options.add_argument("--headless=new")
#         edge_options.add_argument("--disable-gpu")
#         edge_options.add_argument("--window-size=1920,1080")
#         edge_options.add_argument("--start-maximized")
#         edge_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36")
#         edge_service = Service('/usr/local/bin/msedgedriver')
#         driver = webdriver.Edge(service=edge_service, options=edge_options)
#         return driver

def check_whatsapp(driver):
    check = False
    driver.get("https://web.whatsapp.com")
    
    sleep(20)
    
    title = driver.title
    print(f"Page title: {title}")  # Debugging line to check the actual title
    
    if re.search(r"\(\d+\) WhatsApp", title):
        print("Already logged in")
        check = True
        return {"status_code": 200, "Check": f"{check}"}
    elif title == "WhatsApp":
        print ("Not logged in")
        check = False
        return {"status_code": 200, "Check": f"{check}"}
    else:
        return {"status_code": 500, "message": "Unexpected title, cannot determine login status"}

def open_whatsapp(driver, phone_no):
    # Navigate to WhatsApp Web
    Check = False
    driver.get("https://web.whatsapp.com")
    
    # Wait for the page to load
    sleep(20)

    # Check if the chat list is present to determine if logged in
    try: 
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Chat list']"))
        )
        print("Already logged in")
        Check = True
        return {"status_code": 200, "message": "WhatsApp Web is already logged in", "Check": Check }
    
    except Exception as e:
        # Element not found, assume not logged in
        print("No Element found...")
        print("Not logged in")
        result = handle_code(driver, phone_no)
        # sleep(10)  # Allow time for handling
        return result


def handle_code(driver, phone_no):
    try:
        # Wait for the page to load and the code element to be present
        time.sleep(15)  # Adjust based on your network speed and system performance
        
        # Click the link to start the process
        phone_number_link = '/html/body/div[1]/div/div/div[2]/div[3]/div[1]/div/div/div[3]/div/span'
        link_element = wait_and_find(driver, By.XPATH, 'phone_number_link', phone_number_link, 5)
        if isinstance(link_element, dict):  # Check if the function returned a status message
            return link_element
        link_element.click()
        
        # Wait for the new elements to be visible
        time.sleep(5)
        
        # Enter the phone number
        phone_number = '/html/body/div[1]/div/div/div[2]/div[3]/div[1]/div/div[3]/div[1]/div[2]/div/div/div/form/input'
        phone_number_input = wait_and_find(driver, By.XPATH, 'phone_number', phone_number, 5)
        if isinstance(phone_number_input, dict):  # Check if the function returned a status message
            return phone_number_input
        phone_number_input.send_keys(phone_no)
        time.sleep(6)
        
        # Click the next button
        next = '/html/body/div[1]/div/div/div[2]/div[3]/div[1]/div/div[3]/div[2]/button'
        next_button = wait_and_find(driver, By.XPATH, 'next', next, 5)
        if isinstance(next_button, dict):  # Check if the function returned a status message
            return next_button
        next_button.click()
        
        # Wait for the code to be displayed
        time.sleep(15)  # Adjust based on how long it takes to receive the code
        
        # Locate the div element containing the data-link-code attribute
        code_box = '/html/body/div[1]/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div/div'
        code_element = wait_and_find(driver, By.XPATH, 'code_box', code_box, 10)
        if isinstance(code_element, dict):  # Check if the function returned a status message
            return code_element
        
        # Extract the value of the data-link-code attribute
        code = code_element.get_attribute('data-link-code')
        
        if code:
            # Split the code by commas
            code_parts = code.split(',')
            # Format the code into the desired format
            formatted_code = ' '.join(code_parts[:4]) + ' - ' + ' '.join(code_parts[4:])
            print(f"Requested code: {formatted_code}")
            input("Please enter the code in your mobile app and press Enter when done...")
        else:
            print("No code found. Please check the XPath or the page structure.")
            return {"status_code": 500, "message": "No code found"}
        
        return {"status_code": 200, "message": "Code displayed and user prompted"}

    except Exception as e:
        return {"status_code": 500, "message": f"Error handling code: {str(e)}"}
    





# Function to open a channel and send an image with a caption
def open_channel(driver, channel_name):
    try:
        channel_button_xpath = '/html/body/div[1]/div/div/div[2]/header/div/div/div/div/span/div/div[1]/div[3]/div'
        channel_button = wait_and_find(driver, By.XPATH, 'channel_button_xpath', channel_button_xpath, 20)
        if isinstance(channel_button, dict):  # Check if the function returned a status message
            return channel_button
        
        channel_button.click()

        test_channel_xpath = f'//span[@title="{channel_name}"]'
        test_channel = wait_and_find(driver, By.XPATH, 'test_channel_xpath', test_channel_xpath, 20)
        if isinstance(test_channel, dict):  # Check if the function returned a status message
            return test_channel
        
        test_channel.click()
        sleep(6)
        return {"status_code": 200, "message": f"Channel '{channel_name}' opened successfully"}
    except Exception as e:
        return {"status_code": 500, "message": f"Error opening channel '{channel_name}'"}




# Function to send an image with a caption to a group
def send_image_with_caption(driver, image_paths, caption):
    try:
        # JavaScript function to set caption and send the image
        send_image_script = """
        function setCaption(caption) {
            const mainEl = document.querySelector('#main');
            const captionEl = mainEl.querySelector('div[contenteditable="true"]');
    
            if (!captionEl) {
                throw new Error('Unable to find caption input field');
            }
    
            // Split the caption by newlines
            const lines = caption.split('\\n');
    
            // Clear existing content
            captionEl.innerHTML = '';
    
            // Function to insert text and simulate Shift+Enter
            function insertTextWithShiftEnter(text) {
                const range = document.createRange();
                const sel = window.getSelection();
                range.setStart(captionEl, captionEl.childNodes.length);
                range.collapse(true);
                sel.removeAllRanges();
                sel.addRange(range);
        
                // Insert the text
                document.execCommand('insertText', false, text);
            }
    
            // Insert each line followed by Shift+Enter
            for (let i = 0; i < lines.length; i++) {
                insertTextWithShiftEnter(lines[i]);
                if (i < lines.length - 1) {
                    // Insert a newline (Shift+Enter)
                    const event = new KeyboardEvent('keydown', {
                        key: 'Enter',
                        code: 'Enter',
                        keyCode: 13,
                        which: 13,
                        shiftKey: true
                    });
                    captionEl.dispatchEvent(event);
                }
            }
    
            // Trigger a change event to ensure any listeners are updated
            captionEl.dispatchEvent(new Event('change', { bubbles: true }));
        }

        // Example usage
        setCaption(arguments[0]);
        """

        # Execute the JavaScript function with the caption as an argument
        driver.execute_script(send_image_script, caption)
        print("Script executed")

        if image_paths is not None:
            # Wait until the chat input box is visible
            chat = '//div[@title="Attach"]'
            chat_box = wait_and_find(driver, By.XPATH, 'chat', chat, 30)
            if isinstance(chat_box, dict):  # Check if the function returned a status message
                return chat_box
            sleep(3)
            # Click on the attach icon
            # attach = '//div[@title="Attach"]'
            # attach_icon = wait_and_find(driver, By.XPATH, 'attach', attach, 2)
            # if isinstance(attach_icon, dict):  # Check if the function returned a status message
            #     return attach_icon
            # attach_icon.click()

            # # Wait for the "Attach" button to load, and click the image attachment option
            # media_attach = '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'
            # image_attach_option = wait_and_find(driver, By.XPATH, 'media_attach', media_attach, 10)
            # if isinstance(image_attach_option, dict):  # Check if the function returned a status message
            #     return image_attach_option

            # # Send the file path to the image attach input
            # image_attach_option.send_keys(image_path)

            # sleep(5)

            # send_button_xpath = "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]/div/div"
            # send_button = wait_and_find(driver, By.XPATH, 'send_button_xpath', send_button_xpath, 5)
            # if isinstance(send_button, dict):  # Check if the function returned a status message
            #     return send_button
        
            # send_button.click()
            # print("Send button with image clicked")
            # sleep(10)

            driver.save_screenshot("ss2.png")
            attach = '//div[@title="Attach"]'

            attach_icon = wait_and_find(driver, By.XPATH, 'attach', attach, 2)

            if isinstance(attach_icon, dict):  # Check if the function returned a status message

                return attach_icon

            attach_icon.click()
            all_images = "\n".join(os.path.abspath(image) for image in image_paths)
            media_attach = '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'

            image_attach_option = wait_and_find(driver, By.XPATH, 'media_attach', media_attach, 10)

            if isinstance(image_attach_option, dict):  # Check if the function returned a status message

                return image_attach_option

            image_attach_option.send_keys(all_images)

            time.sleep(4)

            send_button_xpath = "/html/body/div[1]/div/div/div[2]/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]/div/div"

            send_button = wait_and_find(driver, By.XPATH, 'send_button_xpath', send_button_xpath, 2)

            if isinstance(send_button, dict):  # Check if the function returned a status message

                return send_button
            driver.save_screenshot("ss.png")

            send_button.click()

            time.sleep(30)
        else:
            send_button_text_xpath = "/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button"
            send_button_text = wait_and_find(driver, By.XPATH, 'send_button_text_xpath', send_button_text_xpath, 5)
            if isinstance(send_button_text, dict):  # Check if the function returned a status message
                return send_button
        
            send_button_text.click()
            print("SEND button clicked!")
            sleep(10)

        return {"status_code": 200, "message": "Media with caption sent successfully"}

    except Exception as e:
        return {"status_code": 500, "message": f"Error sending image with caption: {str(e)}"}


# Function to select a group by name
def select_group(driver, group_name):
    try:
        search = '//div[@contenteditable="true"][@data-tab="3"]'
        search_box = wait_and_find(driver, By.XPATH, 'search', search, 20)
        if isinstance(search_box, dict):  # Check if the function returned a status message
            return search_box
        print("Search done")
        search_box.clear()
        search_box.send_keys(group_name)
        
        group_xpath = f'//span[@title="{group_name}"]'
        group_element = wait_and_find(driver, By.XPATH, 'group_xpath', group_xpath, 20)
        if isinstance(group_element, dict):  # Check if the function returned a status message
            return group_element
        
        group_element.click()
        print("Clicked and group opened")

        return {"status_code": 200, "message": f"Group '{group_name}' selected successfully"}
    except Exception as e:
        return {"status_code": 500, "message": f"Error selecting group '{group_name}'"}


    



# Function to wait for an element and find it
def wait_and_find(driver, by, variable_name, value, timeout=10):
    try:
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        # return element
    except Exception as e:
        return {"status_code": 404, "message": f"{variable_name} (Variable) Element not found: {value}"}
    





