from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LeaveRequestSerializer
from .functions import send_email, add_leave_request, send_data_to_frontend, update_employee_status
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status




class LineManagerAPI(APIView):
    #this get method will be from line manager
    def get(self,request):
        # department = request.data.get('department')

        department = request.query_params.get('department')
        # data = request.data  # Get the data sent in the body of the POST request
        # print("Received data:", data)  # Print the received data to the console
        
        # Optionally process the data here
        data = send_data_to_frontend(department)
        return Response(data, status=status.HTTP_200_OK)
    

    # status will be updated line manager will send the status(approved or declined)
    def put(self,request):
        # get the status and emp_id
        leave_request_status = request.data.get('status')
        emp_id = request.data.get('emp_id')

        # Check if both status and emp_id are provided
        if not leave_request_status or not emp_id:
            return Response({"error": "Both 'status' and 'emp_id' are required."}, status=status.HTTP_400_BAD_REQUEST)

        # find the employee to update status
        try:
            result = update_employee_status(emp_id,leave_request_status)
            print(result)
        except Exception as error:
            return Response({"error" : f"error occured {error}"})

        return Response({'message' : 'status updated successfully'},status=status.HTTP_200_OK)


# getting data from user(frontend) and storing it into database
class LeaveRequestAPI(APIView):
    def post(self, request):
        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            emp_id = serializer.validated_data.get('emp_id')
            emp_name = serializer.validated_data.get('emp_name')
            leave_date = serializer.validated_data.get('leave_date')
            leave_reason = serializer.validated_data.get('leave_reason')
            sender_email = serializer.validated_data.get('sender_email')
            sender_password = serializer.validated_data.get('sender_password')
            body = serializer.validated_data.get('email_body')
            subject = serializer.validated_data.get('email_subject')
            department = serializer.validated_data.get('department')

            print(sender_email)
            print(sender_password)
        
            hr_email = "de.naqeeb@brbgroup.pk"
            line_manager_email = "de.naqeeb@brbgroup.pk"

            recipients = [hr_email, line_manager_email]

            if not all([emp_id, emp_name, leave_date, sender_email, sender_password, body, department]):
                return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

            success, error_message = send_email(subject, body, recipients, str(sender_email), str(sender_password))
            if not success:
                return Response({"send_email error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            success, error_message = add_leave_request(emp_id, leave_date, leave_reason, body, department)
            
            if not success: 
                return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"success_message": "Leave request submitted and email sent successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

