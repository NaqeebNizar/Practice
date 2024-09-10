from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LeaveRequestSerializer
from .functions import send_email, add_leave_request, get_employee_details, send_data_to_frontend, send_filter_data_to_frontend, update_leave_request_status, check_pin_validation, get_line_manager_email, send_updated_email, get_line_manager_email_and_password
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import status


# for HR getting all the data to frontend from leave_requests table
class GetLeaveRequestData(APIView):
    def post(self, request):
        data = send_data_to_frontend()
        return Response(data,status=HTTP_200_OK)




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
        return Response(result)

        # if leave_status == 'Approved':
        #     recipients = ['de.naqeeb@brbgroup.pk'] # get the hr email

            # line manager will send the email to HR
            # so we need to find the line manager of that department first
            # Get the line manager email and password
            # line_manager_email, line_manager_password, error_message = get_line_manager_email_and_password(department)
            
  
            
            # if line_manager_password and line_manager_password:
            #     print(f"{line_manager_email} {line_manager_password}")
            # return Response({"error" : error_message}, status=HTTP_400_BAD_REQUEST)
            #     email_success, email_error = send_updated_email(email_subject, approved_email_body, recipients, str(line_manager_email))
            #     if email_success:
            #         return Response(email_success)
            # return Response(email_error)
        # return Response({"message": f"{error_message} Leave request status updated successfully."}, status=HTTP_200_OK)
        # else:
        #     return Response({"error": message}, status=HTTP_400_BAD_REQUEST)
        




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
                return Response({"error": "Employee not found in the database. Please provide all details."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # If emp_id is not provided, return an error
            return Response({"error": "Employee ID is required"}, status=status.HTTP_400_BAD_REQUEST)




# getting data from user(frontend) and storing it into database
class LeaveRequestAPI(APIView):
    def post(self, request):
        emp_id = request.data.get('emp_id')
        emp_name = request.data.get('emp_name')
        leave_start_date = request.data.get('leave_start_date') # new field
        leave_end_date = request.data.get('leave_end_date') # new field
        # leave_duration = request.data.get('leave_duration') # new field
        leave_reason = request.data.get('leave_reason')
        sender_email = request.data.get('sender_email')
        sender_password = request.data.get('sender_password')
        body = request.data.get('email_body')
        subject = request.data.get('email_subject')
        department = request.data.get('department')

        
        hr_email = "de.naqeeb@brbgroup.pk" # currently hardcoded

        # get the line manager email for a specific department for departments table
        # get the department from user and then match 
        line_manager_email = get_line_manager_email(department)
        print(line_manager_email)
        

        recipients = [hr_email,line_manager_email]

        if not all([emp_id, emp_name, leave_start_date, leave_end_date, leave_reason, sender_email, sender_password, body, subject, department]):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
        success, error_message = send_email(subject, body, recipients, str(sender_email), str(sender_password))
        if not success:
            return Response({"send_email error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        success, error_message = add_leave_request(emp_id, leave_start_date, leave_end_date, leave_reason, department)
            
        if not success: 
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"success_message": "Leave request submitted and email sent successfully."}, status=status.HTTP_200_OK)





# class Home(APIView):
#     def get(self, request):
#         print("Home view accessed")  # For debugging
#         return Response({'message': "success"}, status=status.HTTP_200_OK)

