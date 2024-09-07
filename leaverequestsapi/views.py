from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LeaveRequestSerializer
from .functions import send_email, add_leave_request, send_data_to_frontend
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status





class LineManagerAPI(APIView):
    #this get method will be from line manager
    def post(self,request):
        data = request.data  # Get the data sent in the body of the POST request
        print("Received data:", data)  # Print the received data to the console
        
        # Optionally process the data here
        data = send_data_to_frontend()
        return Response({"message": "Data sent to frontend successfully.",
                             "data" : data,
                            }, status=status.HTTP_200_OK)

        # return Response({'received_data': data}, status=status.HTTP_200_OK)



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
            line_manager_email = "naqeebnizarali@gmail.com"

            recipients = [hr_email, line_manager_email]

            if not all([emp_id, emp_name, leave_date, sender_email, sender_password, department]):
                return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

            success, message = send_email(subject, body, recipients, str(sender_email), str(sender_password))
            if not success:
                return Response({"send_email error": message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            success, message = add_leave_request(emp_id, leave_date, leave_reason, department)
            
            if not success: 
                return Response({"error": message}, status=status.HTTP_400_BAD_REQUEST)

            data = send_data_to_frontend()
            print(data)
            return Response({"message": "Leave request submitted and email sent successfully.",
                             "data" : data,
                            }, status=status.HTTP_200_OK)

            # return Response({"message": "Leave request submitted and email sent successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





