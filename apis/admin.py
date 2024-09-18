from django.contrib import admin
from .models import employees,Departments,leave_requests,leave_tracking

# Register your models here.
admin.site.register(employees)
admin.site.register(Departments)
admin.site.register(leave_requests)
admin.site.register(leave_tracking)
