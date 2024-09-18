from rest_framework import serializers
from .models import employees, leave_tracking,leave_requests ,Departments # Replace with your actual model import


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = employees
        fields = '__all__'


# class UploadedImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UploadedImage
#         fields = ['image']


class LeaveTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = leave_tracking
        fields = '__all__'  # Or specify the fields you want to serialize




class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = leave_requests
        fields = '__all__'  # Or specify the fields you want to serialize



class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'