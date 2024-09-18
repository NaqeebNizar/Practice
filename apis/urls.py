from django.urls import path
from . import views
from .views import LeaveRequestAPI ,GetFilteredData,EditEmployeeData, NotifyEmployee, GetLeaveRequestData, GetPin, UpdateLeaveRequestData, AutoFillData
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('add_leave_request/',LeaveRequestAPI.as_view(),name="add-leave-request"),
    path('get_pin/',GetPin.as_view(),name="get-and-verify-pin"),
    path('get_leave_request/',GetLeaveRequestData.as_view(),name="get-leave-request_data"),
    path('get_filtered_data/',GetFilteredData.as_view(),name="get-filtered-data"),
    path('update_leave_request_data/',UpdateLeaveRequestData.as_view(),name="update-leave-request-data"),
    path('emp_id/',AutoFillData.as_view(),name="auto-fill-data"),
    path('notify_employee/',NotifyEmployee.as_view(),name="notify-email"),
    path('employees/<int:emp_id>/', EditEmployeeData.as_view(), name='update-employee'),
    # path('get_employee_details/',GetEmployees.as_view(),name='get-employees'),
    # path('upload_image/', UploadImage.as_view(), name='upload_image'),
    # path('tier/',ApprovalTierView.as_view(),name='tier'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)