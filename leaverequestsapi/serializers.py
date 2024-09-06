from rest_framework import serializers
from .models import LeaveRequest  # Replace with your actual model import

class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest  # Replace with your actual model name
        fields = ['emp_id', 'emp_name', 'leave_date', 'leave_reason', 'sender_email', 'sender_password', 'email_body', 'email_subject', 'department']
