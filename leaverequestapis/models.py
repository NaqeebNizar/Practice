from django.db import models

# Create your models here.

from django.db import models
# Create your models here.

# class test(models.Model):
#     title = models.CharField(max_length=200)
#     string = models.CharField(max_length=100)
#     def __str__(self):
#         return self.title

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')

    def __str__(self):
         return self.image

class PostsOnSocialMedias(models.Model):
    Social_Media = models.TextField()
    image = models.ImageField(upload_to= 'uploads/')
    PostText = models.TextField()
    title = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.Social_Media


class daily_attendance(models.Model):
    emp_id = models.CharField(max_length=9,unique=False)
    emp_name = models.CharField(max_length=100)
    date = models.DateField()
    time_in = models.TimeField(null = True, blank= True)
    time_out = models.TimeField(null = True, blank= True)
    status = models.TextField()
    location = models.CharField(max_length=100, null = True, blank= True)
    department = models.CharField(max_length=50, blank=True)
    StartShiftTimings = models.CharField(max_length= 50, null = True, blank= True)
    EndShiftTimings = models.CharField(max_length= 50, null = True, blank= True)
    LateStart = models.BooleanField(default = False, null = True, blank= True)
    EarlyOut = models.BooleanField(default = False, null = True, blank= True)

    class Meta:
        unique_together = ('emp_id', 'date')
         
class employees(models.Model):
    id = models.CharField(max_length=10 ,primary_key=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True, null = True)
    location = models.CharField(max_length=100, null = True, blank= True)  
    StartShiftTimings = models.CharField(max_length=50, null= True, blank= True)
    EndShiftTimings = models.CharField(max_length=50, null= True, blank= True)
    designation = models.CharField(max_length=50, null= True, blank= True)
    date_of_joining = models.DateField(null=True, blank= True)
    employment_status = models.CharField(max_length=50, null= True, blank= True)
    emp_image = models.ImageField(upload_to='emp_image/', blank=True, null=True)

    def __str__(self):
        return self.name

class Departments(models.Model):
    department_name = models.CharField(max_length=50,primary_key=True)
    manager_name = models.CharField(max_length=50)
    manager_email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    HOD_HR = models.CharField(max_length=60, null= True, blank=True)

    def __str__(self):
        return self.department_name



class leave_requests(models.Model):
    emp_id = models.ForeignKey(employees, on_delete=models.CASCADE)  # ForeignKey to Employees
    leave_date = models.DateField()
    leave_reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    department = models.CharField(max_length=50, blank= True, null= True)  # Treat it as a CharField since it's text
    status = models.CharField(max_length=50,blank=True)
    email_body = models.TextField(blank= True, null= True)
    leave_duration = models.IntegerField(blank= True, null= True)
    timestamp = models.DateTimeField(auto_now_add=True, blank= True, null= True)

    class Meta:
        unique_together = ('emp_id', 'leave_date')
        

class leave_tracking(models.Model):
    emp_id = models.CharField(max_length=10)
    annual_total = models.IntegerField()
    annual_consumed = models.IntegerField()
    annual_remaining = models.IntegerField()
    sick_total = models.IntegerField()
    sick_consumed = models.IntegerField()
    sick_remaining = models.IntegerField()
    casual_total = models.IntegerField()
    casual_consumed = models.IntegerField()
    casual_remaining = models.IntegerField()

    def __str__(self):
        return self.emp_id