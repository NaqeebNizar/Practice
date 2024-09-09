from django.urls import path
from . import views
from .views import LeaveRequestAPI, GetFilteredData, GetLeaveRequestData, GetPin, UpdateLeaveRequestData

urlpatterns = [
    path('add_leave_request/',LeaveRequestAPI.as_view(),name="add-leave-request"),
    path('get_pin/',GetPin.as_view(),name="get-and-verify-pin"),
    path('get_leave_request/',GetLeaveRequestData.as_view(),name="get-leave-request_data"),
    path('get_filtered_data/',GetFilteredData.as_view(),name="get-filtered-data"),
    path('update_leave_request_data/',UpdateLeaveRequestData.as_view(),name="update-leave-request-data"),
    # path('index/',Home.as_view(),name="index"),
]
