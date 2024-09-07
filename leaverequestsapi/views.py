from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LeaveRequestSerializer
from .functions import send_email, add_leave_request, send_data_to_frontend, update_employee_status, send_filter_data_to_frontend
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status




# getting all the data
class GetLeaveRequestData(APIView):
    def post(self, request):
        data = send_data_to_frontend()
        return Response(data,status=status.HTTP_200_OK)




# for handling pin authentication
class GetFilteredData(APIView):
    #this get method will be from line manager
    def post(self,request):
        # get the pin from frontend and then match it to the department
        pin = request.data.get('pin')
        data = send_filter_data_to_frontend(pin)
        return Response(data, status=status.HTTP_200_OK)




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




class Home(APIView):
    def get(self, request):
        print("Home view accessed")  # For debugging
        return Response({'message': "success"}, status=status.HTTP_200_OK)

