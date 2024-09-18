# from django.shortcuts import get_object_or_404, render
# from rest_framework.views import APIView
# # from .serializers import LeaveRequestSerializer
# from .functions import send_email, add_leave_request,calculate_leave_tracking, send_data_to_frontend, get_employee_details, send_filter_data_to_frontend, get_employee_email, update_leave_request_status, employee_send_email, check_pin_validation, get_line_manager_email
# # from django.views.decorators.csrf import csrf_exempt
# from rest_framework.response import Response
# from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR


# # for HR getting all the data to frontend from leave_requests table
# class GetLeaveRequestData(APIView):
#     def post(self, request):
#         data = send_data_to_frontend()
#         return Response(data,status=HTTP_200_OK)
    


# # HR will send an email to the employee
# class NotifyEmployee(APIView):
#     def post(self, request):
#         emp_id = request.data.get('emp_id')
#         deparment = request.data.get('department')
#         email_body = request.data.get('email_body')
#         email_subject = request.data.get('email_subject')
#         leave_duration = request.data.get("leave_duration")
#         leave_type = request.data.get('leave_type')
        
        
#         # HR will send an email to the employee(original email) with their dummy email
#         HR_email = "de.naqeeb@brbgroup.pk" # dummy HR email
#         employee_email = get_employee_email(emp_id)
        
#         print(employee_email)

#         line_manager_email = get_line_manager_email(deparment)
#         if isinstance(line_manager_email, tuple):
#             line_manager_email = line_manager_email[0]
#         print(line_manager_email)

#         recipients = [employee_email,line_manager_email]

#         # Call the calculation function
#         data = calculate_leave_tracking(emp_id, leave_duration, leave_type)
        

#         success, error_message = send_email(email_subject, email_body, recipients, "HR", HR_email, "DeNaqeeb@321")
#         if not success:
#             return Response({"send_email error": error_message}, status=HTTP_500_INTERNAL_SERVER_ERROR)
#         print(success)
#         return Response(data)
    

        

        



# # for handling pin authentication and will return the data of the employees from
# # departments and leave_requests table where department = pin(password) and where
# # status = Pending 
# class GetFilteredData(APIView):
#     # this get method will be from line manager
#     def post(self,request):
#         # get the pin from frontend and then match it to the department
#         pin = request.data.get('pin')

#         # get the filtered data of the employees based on specific
#         # department and status = Pending
#         data = send_filter_data_to_frontend(pin)
#         print(data)
#         return Response(data, status=HTTP_200_OK)



# class GetPin(APIView):
#     def post(self, request):
#         # get the pin from frontend and then match it to the department
#         pin = request.data.get('pin')
#         message = check_pin_validation(pin)
#         return Response(message)



# # for updating the employees leave_request data in the leave_requests table
# class UpdateLeaveRequestData(APIView):
#     def put(self,request):
#         # get the emp_id and updated status from the line manager
#         leave_request_id = request.data.get('id')
#         emp_id = request.data.get('userId')
#         status = request.data.get('status')
#         department = request.data.get('department')

#         if status == "Approved":
#             approved_email_body = request.data.get('email_body')
#             email_subject = request.data.get('subject')
#             print(approved_email_body)
#             print(email_subject)
#         elif status == "Declined":
#             declined_email_body = request.data.get('email_body')
#             email_subject = request.data.get('subject')
#             print(declined_email_body)
#             print(email_subject)


#         print(f"{leave_request_id} {emp_id} {status}")

#         # Update the leave request status
#         result = update_leave_request_status(leave_request_id, emp_id, status)
#         print(status)

#         recipients_HR = "de.rabia@brbgroup.pk" # HR email
            
#         # get the line manager email
#         line_manager_email = "de.naqeeb@brbgroup.pk" # line manager dummy email

#         # get the line manager name
#         # line_manager_name = get_line_manager_name(department)
#         if isinstance(line_manager_name, tuple):
#             line_manager_name = line_manager_name[0]
#         print(line_manager_name)

#         if status == "Approved":
#             # line manager will send the email to HR with their dummy email
#             # emp_name and sender_email is passed in f string in send_email function
#             success, error_message = send_email(email_subject, approved_email_body, recipients_HR, line_manager_name, line_manager_email, "DeNaqeeb@321")
#             if not success:
#                 return Response({"send_email error": error_message}, status=HTTP_500_INTERNAL_SERVER_ERROR)            
#             print(success)
#         elif status == "Declined":
#             # line manager will send email to employee with their dummy email
#             # get employees email
#             employee_email = get_employee_email(emp_id)
#             print(employee_email)
#             success, error_message = send_email(email_subject, declined_email_body, employee_email, line_manager_name, line_manager_email, "DeNaqeeb@321")
#             if not success:
#                 return Response({"send_email error": error_message}, status=HTTP_500_INTERNAL_SERVER_ERROR)
#             print(success)
#         return Response(result)

# # for autofill
# class AutoFillData(APIView):
#     def post(self, request):
#         emp_id = request.data.get('emp_id')

#         # Fetch the employee's information from the database based on emp_id
#         if emp_id:
#             employee = get_employee_details(emp_id)  # Implement this function to fetch employee data
#             if employee:
#                 # Auto-fill name, email, and department if employee is found
#                 emp_name = employee['name']
#                 sender_email = employee['email']
#                 department = employee['department']
#                 return Response(employee,status=HTTP_200_OK)
#             else:
#                 # If employee not found, require these fields in the request
#                 return Response({"error": "Employee not found in the database. Please provide all details."}, status=HTTP_400_BAD_REQUEST)
#         else:
#             # If emp_id is not provided, return an error
#             return Response({"error": "Employee ID is required"}, status=HTTP_400_BAD_REQUEST)


# # getting data from user(frontend) and storing it into database
# class LeaveRequestAPI(APIView):
#     def post(self, request):
#         emp_id = request.data.get('emp_id')
#         emp_name = request.data.get('emp_name')
#         leave_start_date = request.data.get('leave_start_date') # new field
#         leave_end_date = request.data.get('leave_end_date') # new field
#         leave_duration = request.data.get('leave_duration') # new field
#         leave_reason = request.data.get('leave_reason')
#         sender_email = request.data.get('sender_email')
#         sender_password = request.data.get('sender_password')
#         body = request.data.get('email_body')
#         subject = request.data.get('email_subject')
#         department = request.data.get('department')

        
#         hr_email = "de.rabia@brbgroup.pk" # currently hardcoded will be the original email
#         # line_manager_email = "de.naqeeb@brbgroup.pk"


#         # get the line manager email for a specific department for departments table
#         # get the department from user and then match 
#         line_manager_email = get_line_manager_email(department) # will be the original email
#         if isinstance(line_manager_email, tuple):
#             line_manager_email = line_manager_email[0]
#         print(line_manager_email)
        
#         recipients = [hr_email,line_manager_email]

#         if not all([emp_id, emp_name, leave_start_date, leave_end_date, leave_reason, sender_email, sender_password, body, subject, department]):
#             return Response({"error": "All fields are required"}, status=HTTP_400_BAD_REQUEST)
#         success, error_message = employee_send_email(subject, body, recipients, emp_name, sender_email, sender_password)
#         if not success:
#             return Response({"send_email error": error_message}, status=HTTP_500_INTERNAL_SERVER_ERROR)

#         success, error_message = add_leave_request(emp_id, leave_start_date, leave_end_date, leave_duration, leave_reason, department)
            
#         if not success: 
#             return Response({"error": error_message}, status=HTTP_400_BAD_REQUEST)

#         return Response({"success_message": "Leave request submitted and email sent successfully."}, status=HTTP_200_OK)






from .serializers import EmployeeSerializer, DepartmentSerializer, LeaveTrackingSerializer
from rest_framework.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from .models import employees, leave_tracking, Departments, leave_requests
from rest_framework import status
from rest_framework.views import APIView


# class Add(APIView):
#     def put(self, request, emp_id):
#         try:
#             # Retrieve the employee instance using 'id' instead of 'emp_id'
#             employee = employees.objects.get(id=emp_id)
#         except employees.DoesNotExist:
#             return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

#         # Deserialize and validate the employee data
#         employee_data = request.data.get('employee', {})
#         serializer = EmployeeSerializer(employee, data=employee_data, partial=True)
#         if serializer.is_valid():
#             # Save the updated employee instance
#             serializer.save()
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         # Handle leave tracking data
#         leave_tracking_data = request.data.get('leave_tracking', {})
#         try:
#             leave_tracking_instance = leave_tracking.objects.get(emp_id=emp_id)
#             leave_tracking_serializer = LeaveTrackingSerializer(leave_tracking_instance, data=leave_tracking_data, partial=True)
#             if leave_tracking_serializer.is_valid():
#                 leave_tracking_serializer.save()
#             else:
#                 return Response(leave_tracking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except leave_tracking.DoesNotExist:
#             leave_tracking_data['emp_id'] = emp_id
#             leave_tracking_serializer = LeaveTrackingSerializer(data=leave_tracking_data)
#             if leave_tracking_serializer.is_valid():
#                 leave_tracking_serializer.save()
#             else:
#                 return Response(leave_tracking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         # Update department information
#         department_data = {
#             'manager_name': request.data.get('manager_name'),
#             'HOD_HR': request.data.get('HOD_HR')
#         }
#         department_name = employee.department
#         try:
#             department_instance = Departments.objects.get(department_name=department_name)
#             department_serializer = DepartmentSerializer(department_instance, data=department_data, partial=True)
#             if department_serializer.is_valid():
#                 department_serializer.save()
#             else:
#                 return Response(department_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Departments.DoesNotExist:
#             return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)

#         return Response({
#             'employee': serializer.data,
#             'leave_tracking': leave_tracking_serializer.data,
#             'department': department_serializer.data
#         }, status=status.HTTP_200_OK)






# class Add(APIView):
#     def put(self, request, emp_id):
#         try:
#             # Retrieve the employee instance using 'id' instead of 'emp_id'
#             employee = employees.objects.get(id=emp_id)
#         except employees.DoesNotExist:
#             return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

#         # Deserialize and validate the employee data
#         employee_data = request.data.get('employee', {})
#         serializer = EmployeeSerializer(employee, data=employee_data, partial=True)  # partial=True allows partial updates
#         if serializer.is_valid():
#             # Save the updated employee instance
#             serializer.save()
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         # Handle leave tracking data
#         leave_tracking_data = request.data.get('leave_tracking', {})
#         try:
#             leave_tracking_instance = leave_tracking.objects.get(emp_id=emp_id)
#             leave_tracking_serializer = LeaveTrackingSerializer(leave_tracking_instance, data=leave_tracking_data, partial=True)
#             if leave_tracking_serializer.is_valid():
#                 leave_tracking_serializer.save()
#             else:
#                 return Response(leave_tracking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except leave_tracking.DoesNotExist:
#             leave_tracking_data['emp_id'] = emp_id
#             leave_tracking_serializer = LeaveTrackingSerializer(data=leave_tracking_data)
#             if leave_tracking_serializer.is_valid():
#                 leave_tracking_serializer.save()
#             else:
#                 return Response(leave_tracking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         # Handle department data
#         department_data = request.data.get('department', {})
#         department_name = employee.department
#         try:
#             department_instance = Departments.objects.get(department_name=department_name)
#             department_serializer = DepartmentSerializer(department_instance, data=department_data, partial=True)
#             if department_serializer.is_valid():
#                 department_serializer.save()
#             else:
#                 return Response(department_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Departments.DoesNotExist:
#             return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)

#         return Response({
#             'employee': serializer.data,
#             'leave_tracking': leave_tracking_serializer.data,
#             'department': department_serializer.data
#         }, status=status.HTTP_200_OK)


from PIL import Image
import os
class EditEmployeeData(APIView):
    def put(self, request, emp_id):
        try:
            # Retrieve the employee instance using 'id' instead of 'emp_id'
            employee = employees.objects.get(id=emp_id)
            image = request.FILES.get('emp_image')
            print(employee)
        except employees.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Deserialize and validate the employee data
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)  # partial=True allows partial updates
        if serializer.is_valid():
            # Save the updated employee instance
            serializer.save()
            if image:
                # get the current image to delete it later if necessary
                old_image = employee.emp_image.path if employee.emp_image else None

                # save the new image if an image already exists
                employee.emp_image = image
                employee.save()

                # optional delete the old image
                if old_image and os.path.isfile(old_image):
                    os.remove(old_image)

                # Get the image URL
                image_url = employee.emp_image.url
                print("Image URL:", image_url)
            else:
                print("No image provided")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Handle leave tracking data
        # leave_tracking_data = request.data.get('leave_tracking', {})
        try:
            leave_tracking_instance = leave_tracking.objects.get(emp_id=emp_id)
            print(leave_tracking_instance)
            leave_tracking_serializer = LeaveTrackingSerializer(leave_tracking_instance, data=request.data, partial=True)
            if leave_tracking_serializer.is_valid():
                leave_tracking_serializer.save()
            else:
                return Response(leave_tracking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except leave_tracking.DoesNotExist:
            # leave_tracking_data['emp_id'] = emp_id
            # leave_tracking_serializer = LeaveTrackingSerializer(data=leave_tracking_data)
            # if leave_tracking_serializer.is_valid():
            #     leave_tracking_serializer.save()
            # else:
            #     return Response(leave_tracking_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            pass
        # Handle department data
        department_name = employee.department
        try:
            department_instance = Departments.objects.get(department_name=department_name)
            print(department_instance)
            department_serializer = DepartmentSerializer(department_instance, data=request.data, partial=True)
            if department_serializer.is_valid():
                department_serializer.save()
            else:
                return Response(department_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Departments.DoesNotExist:
            return Response({'error': 'Department not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'employee': serializer.data,
            'leave_tracking': leave_tracking_serializer.data,
            'department': department_serializer.data
        }, status=status.HTTP_200_OK)
        









# # get employees details
# class AddEmployees(APIView):
#     # def post(self, request):
#     #     serializer = EmployeeSerializer(data=request.data)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response({'message': 'Employee data saved successfully'}, status=HTTP_201_CREATED)
#     #     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    

#     # def post(self, request):
#     #     serializer = DepartmentSerializer(data=request.data)
#     #     if serializer.is_valid():
#     #         serializer.save()
#     #         return Response({'message': 'Departments data saved successfully'}, status=HTTP_201_CREATED)
#     #     return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


#     def post(self, request):
#         serializer = DepartmentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'leave_requests data saved successfully'}, status=HTTP_201_CREATED)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    


# from .serializers import LeaveTrackingSerializer

# class GetEmployees(APIView):
#     def post(self, request):
#         emp_id = request.data.get('emp_id')
#         image = request.FILES.get('image')  # Get the uploaded image file

#         try:
#             # Retrieve the employee based on ID
#             employee = employees.objects.get(id=emp_id)

#             # Construct the image URL for the frontend
#             # Update the employee's image if an image is provided
#             image_url = None
#             if image:
#                 image_url = request.build_absolute_uri(employee.image.url)
#                 employee.image.save(image_url, image)  # Save the image to the employee instance
#                 employee.save()  # Make sure to save the employee instance after adding the image
            
#             # Serialize the employee data
#             serializer2 = EmployeeSerializer(employee)

#             # Retrieve leave tracking information
#             data = leave_tracking.objects.get(emp_id=emp_id)
#             serializer = LeaveTrackingSerializer(data)

            
#             # Format the response as desired
#             formatted_data = {
#                 "annualleave": {
#                     "total": serializer.data.get('annual_total', 0),
#                     "consume": serializer.data.get('annual_consumed', 0),
#                     "remaining": serializer.data.get('annual_remaining', 0),
#                 },
#                 "casualleave": {
#                     "total": serializer.data.get('casual_total', 0),
#                     "consume": serializer.data.get('casual_consumed', 0),
#                     "remaining": serializer.data.get('casual_remaining', 0),
#                 },
#                 "sickleave": {
#                     "total": serializer.data.get('sick_total', 0),
#                     "consume": serializer.data.get('sick_consumed', 0),
#                     "remaining": serializer.data.get('sick_remaining', 0),
#                 },
#             }

#             return Response({"Employee data": serializer2.data, "Employee leaves": formatted_data})
#         except employees.DoesNotExist:
#             return Response({"error": "Employee not found"}, status=HTTP_404_NOT_FOUND)
        


# from django.http import JsonResponse
# class ApprovalTierView(APIView):
#     def get(self, request):
#         emp_id = request.data.get('emp_id')

#         try:
#             employee = employees.objects.get(emp_id=emp_id)
#             department = employee.department
#             return JsonResponse({'department': department}, status=200)
#         except employee.DoesNotExist:
#             return JsonResponse({'error': 'Employee not found'}, status=404)








# # class UploadImage(APIView):
# #     def post(self, request):
# #         # Use the serializer to validate and save the uploaded image
# #         serializer = UploadedImageSerializer(data=request.data)
        
# #         if serializer.is_valid():
# #             serializer.save()  # Save the image to the database
# #             return Response({'message': 'Image uploaded successfully'}, status=HTTP_201_CREATED)
# #         else:
# #             return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)






















from django.shortcuts import render
from rest_framework.views import APIView
# from .serializers import LeaveRequestSerializer
from .functions import send_email,calculate_leave_tracking, send_data_to_frontend, get_line_manager_name,get_employee_details, send_filter_data_to_frontend, get_employee_email, update_leave_request_status, check_pin_validation, get_line_manager_email
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
        # if isinstance(line_manager_name, tuple):
        #     line_manager_name = line_manager_name[0]
        print(line_manager_name)
        employee_name = get_employee_email(emp_id)
        print(employee_name[1])

        if status == "Approved":
            # line manager will send the email to HR with their dummy email
            # emp_name and sender_email is passed in f string in send_email function
            success, error_message = send_email(email_subject, approved_email_body, recipients_HR, line_manager_name, "HR", employee_name,line_manager_email, "DeNaqeeb@321",status)
            if not success:
                return Response({"send_email error": error_message}, status=HTTP_500_INTERNAL_SERVER_ERROR)            
            print(success)
        elif status == "Declined":
            # line manager will send email to employee with their dummy email
            # get employees email
            employee_email = get_employee_email(emp_id)
            print(employee_email)
            success, error_message = send_email(email_subject, declined_email_body, recipients_HR, line_manager_name, "HR", employee_name,line_manager_email, "DeNaqeeb@321",status)
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

        
        hr_email = "de.rabia@brbgroup.pk"  # currently hardcoded
        line_manager_email = get_line_manager_email(department)  # Fetching line manager email

        # Ensure line_manager_email is not None
        if isinstance(line_manager_email, tuple):
            line_manager_email = line_manager_email[0]
        if line_manager_email is None:
            line_manager_email = ""  # Set to empty string if None, or handle as needed

        print(line_manager_email)
        
        recipients = [hr_email, line_manager_email]
        
        # Remove any empty strings from recipients
        recipients = [email for email in recipients if email]

        if not all([emp_id, emp_name, leave_start_date, leave_end_date, leave_reason, sender_email, sender_password, body, subject, department]):
            return Response({"error": "All fields are required"}, status=HTTP_400_BAD_REQUEST)

        success, error_message = send_email(subject, body, recipients, emp_name, sender_email, sender_password)
        if not success:
            return Response({"send_email error": error_message}, status=HTTP_500_INTERNAL_SERVER_ERROR)

        # Uncomment if leave request functionality is needed
        # success, error_message = add_leave_request(emp_id, leave_start_date, leave_end_date, leave_duration, leave_reason, department)
        # if not success:
        #     return Response({"error": error_message}, status=HTTP_400_BAD_REQUEST)

        return Response({"success_message": "Leave request submitted and email sent successfully."}, status=HTTP_200_OK)







# from .serializers import EmployeeSerializer
# from rest_framework.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
# from .models import employees, leave_tracking
# # get employees details
# class AddEmployees(APIView):
#     def post(self, request):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Employee data saved successfully'}, status=HTTP_201_CREATED)
#         return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    





# from .serializers import UploadedImageSerializer, LeaveTrackingSerializer

# class GetEmployees(APIView):
#     def post(self, request):
#         emp_id = request.data.get('emp_id')
#         image = request.FILES.get('image')  # Get the uploaded image file

#         try:
#             # Retrieve the employee based on ID
#             employee = employees.objects.get(id=emp_id)

#             # Construct the image URL for the frontend
#             # Update the employee's image if an image is provided
#             image_url = None
#             if image:
#                 image_url = request.build_absolute_uri(employee.image.url)
#                 employee.image.save(image_url, image)  # Save the image to the employee instance
#                 employee.save()  # Make sure to save the employee instance after adding the image
            
#             # Serialize the employee data
#             serializer2 = EmployeeSerializer(employee)

#             # Retrieve leave tracking information
#             data = leave_tracking.objects.get(emp_id=emp_id)
#             serializer = LeaveTrackingSerializer(data)

            
#             # Format the response as desired
#             formatted_data = {
#                 "annualleave": {
#                     "total": serializer.data.get('annual_total', 0),
#                     "consume": serializer.data.get('annual_consumed', 0),
#                     "remaining": serializer.data.get('annual_remaining', 0),
#                 },
#                 "casualleave": {
#                     "total": serializer.data.get('casual_total', 0),
#                     "consume": serializer.data.get('casual_consumed', 0),
#                     "remaining": serializer.data.get('casual_remaining', 0),
#                 },
#                 "sickleave": {
#                     "total": serializer.data.get('sick_total', 0),
#                     "consume": serializer.data.get('sick_consumed', 0),
#                     "remaining": serializer.data.get('sick_remaining', 0),
#                 },
#             }

#             return Response({"Employee data": serializer2.data, "Employee leaves": formatted_data})
#         except employees.DoesNotExist:
#             return Response({"error": "Employee not found"}, status=HTTP_404_NOT_FOUND)
        


# from django.http import JsonResponse
# class ApprovalTierView(APIView):
#     def get(self, request):
#         emp_id = request.data.get('emp_id')

#         try:
#             employee = employees.objects.get(emp_id=emp_id)
#             department = employee.department
#             return JsonResponse({'department': department}, status=200)
#         except employee.DoesNotExist:
#             return JsonResponse({'error': 'Employee not found'}, status=404)








# class UploadImage(APIView):
#     def post(self, request):
#         # Use the serializer to validate and save the uploaded image
#         serializer = UploadedImageSerializer(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()  # Save the image to the database
#             return Response({'message': 'Image uploaded successfully'}, status=HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



















