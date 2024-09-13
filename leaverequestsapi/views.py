from django.shortcuts import render
from rest_framework.views import APIView
# from .serializers import LeaveRequestSerializer
from .functions import send_email, add_leave_request, get_line_manager_name,calculate_leave_tracking, send_data_to_frontend, get_employee_details, send_filter_data_to_frontend, get_employee_email, update_leave_request_status, employee_send_email, check_pin_validation, get_line_manager_email
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR


# for HR getting all the data to frontend from leave_requests table
class GetLeaveRequestData(APIView):
    def post(self, request):
        data = send_data_to_frontend()
        return Response(data,status=HTTP_200_OK)
    


# HR will send an email to the employee
class NotifyEmployee(APIView):
    def post(self, request):
        emp_id = request.data.get('emp_id')
        deparment = request.data.get('department')
        email_body = request.data.get('email_body')
        email_subject = request.data.get('email_subject')
        leave_duration = request.data.get("leave_duration")
        leave_type = request.data.get('leave_type')
        
        
        # HR will send an email to the employee(original email) with their dummy email
        HR_email = "de.naqeeb@brbgroup.pk" # dummy HR email
        employee_email = get_employee_email(emp_id)
        
        print(employee_email)

        line_manager_email = get_line_manager_email(deparment)
        if isinstance(line_manager_email, tuple):
            line_manager_email = line_manager_email[0]
        print(line_manager_email)

        recipients = [employee_email,line_manager_email]

        # Call the calculation function
        data = calculate_leave_tracking(emp_id, leave_duration, leave_type)
        

        success, error_message = send_email(email_subject, email_body, recipients, "HR", HR_email, "DeNaqeeb@321")
        if not success:
            return Response({"send_email error": error_message}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        print(success)
        return Response(data)
    

        

        



# for handling pin authentication and will return the data of the employees from
# departments and leave_requests table where department = pin(password) and where
# status = Pending 
class GetFilteredData(APIView):
    # this get method will be from line manager
    def post(self,request):
        # get the pin from frontend and then match it to the department
        pin = request.data.get('pin')

        # get the filtered data of the employees based on specific
        # department and status = Pending
        data = send_filter_data_to_frontend(pin)
        print(data)
        return Response(data, status=HTTP_200_OK)



class GetPin(APIView):
    def post(self, request):
        # get the pin from frontend and then match it to the department
        pin = request.data.get('pin')
        message = check_pin_validation(pin)
        return Response(message)



# for updating the employees leave_request data in the leave_requests table
class UpdateLeaveRequestData(APIView):
    def put(self,request):
        # get the emp_id and updated status from the line manager
        leave_request_id = request.data.get('id')
        emp_id = request.data.get('userId')
        status = request.data.get('status')
        department = request.data.get('department')

        if status == "Approved":
            approved_email_body = request.data.get('email_body')
            email_subject = request.data.get('subject')
            print(approved_email_body)
            print(email_subject)
        elif status == "Declined":
            declined_email_body = request.data.get('email_body')
            email_subject = request.data.get('subject')
            print(declined_email_body)
            print(email_subject)


        print(f"{leave_request_id} {emp_id} {status}")

        # Update the leave request status
        result = update_leave_request_status(leave_request_id, emp_id, status)
        print(status)

        recipients_HR = "de.rabia@brbgroup.pk" # HR email
            
        # get the line manager email
        line_manager_email = "de.naqeeb@brbgroup.pk" # line manager dummy email

        # get the line manager name
        line_manager_name = get_line_manager_name(department)
        if isinstance(line_manager_name, tuple):
            line_manager_name = line_manager_name[0]
        print(line_manager_name)

        if status == "Approved":
            # line manager will send the email to HR with their dummy email
            # emp_name and sender_email is passed in f string in send_email function
            success, error_message = send_email(email_subject, approved_email_body, recipients_HR, line_manager_name, line_manager_email, "DeNaqeeb@321")
            if not success:
                return Response({"send_email error": error_message}, status=HTTP_500_INTERNAL_SERVER_ERROR)            
            print(success)
        elif status == "Declined":
            # line manager will send email to employee with their dummy email
            # get employees email
            employee_email = get_employee_email(emp_id)
            print(employee_email)
            success, error_message = send_email(email_subject, declined_email_body, employee_email, line_manager_name, line_manager_email, "DeNaqeeb@321")
            if not success:
                return Response({"send_email error": error_message}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            print(success)
        return Response(result)

# for autofill
class AutoFillData(APIView):
    def post(self, request):
        emp_id = request.data.get('emp_id')

        # Fetch the employee's information from the database based on emp_id
        if emp_id:
            employee = get_employee_details(emp_id)  # Implement this function to fetch employee data
            if employee:
                # Auto-fill name, email, and department if employee is found
                emp_name = employee['name']
                sender_email = employee['email']
                department = employee['department']
                return Response(employee,status=HTTP_200_OK)
            else:
                # If employee not found, require these fields in the request
                return Response({"error": "Employee not found in the database. Please provide all details."}, status=HTTP_400_BAD_REQUEST)
        else:
            # If emp_id is not provided, return an error
            return Response({"error": "Employee ID is required"}, status=HTTP_400_BAD_REQUEST)


# getting data from user(frontend) and storing it into database
class LeaveRequestAPI(APIView):
    def post(self, request):
        emp_id = request.data.get('emp_id')
        emp_name = request.data.get('emp_name')
        leave_start_date = request.data.get('leave_start_date') # new field
        leave_end_date = request.data.get('leave_end_date') # new field
        leave_duration = request.data.get('leave_duration') # new field
        leave_reason = request.data.get('leave_reason')
        sender_email = request.data.get('sender_email')
        sender_password = request.data.get('sender_password')
        body = request.data.get('email_body')
        subject = request.data.get('email_subject')
        department = request.data.get('department')

        
        hr_email = "de.rabia@brbgroup.pk" # currently hardcoded will be the original email
        # line_manager_email = "de.naqeeb@brbgroup.pk"


        # get the line manager email for a specific department for departments table
        # get the department from user and then match 
        line_manager_email = get_line_manager_email(department) # will be the original email
        if isinstance(line_manager_email, tuple):
            line_manager_email = line_manager_email[0]
        print(line_manager_email)
        
        recipients = [hr_email,line_manager_email]

        if not all([emp_id, emp_name, leave_start_date, leave_end_date, leave_reason, sender_email, sender_password, body, subject, department]):
            return Response({"error": "All fields are required"}, status=HTTP_400_BAD_REQUEST)
        success, error_message = employee_send_email(subject, body, recipients, emp_name, sender_email, sender_password)
        if not success:
            return Response({"send_email error": error_message}, status=HTTP_500_INTERNAL_SERVER_ERROR)

        success, error_message = add_leave_request(emp_id, leave_start_date, leave_end_date, leave_duration, leave_reason, department)
            
        if not success: 
            return Response({"error": error_message}, status=HTTP_400_BAD_REQUEST)

        return Response({"success_message": "Leave request submitted and email sent successfully."}, status=HTTP_200_OK)


