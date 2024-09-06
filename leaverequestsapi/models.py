from django.db import models

class LeaveRequest(models.Model):  # Replace with your actual model name
    emp_id = models.CharField(max_length=100)
    emp_name = models.CharField(max_length=100)
    leave_date = models.DateField()
    leave_reason = models.TextField()
    sender_email = models.EmailField()
    sender_password = models.CharField(max_length=100)
    email_body = models.TextField()
    email_subject = models.CharField(max_length=255)
    department = models.CharField(max_length=50)  # New field

    def __str__(self):
        return f"{self.emp_name} - {self.leave_date}"
