from django.urls import path
from . import views
from .views import LeaveRequestAPI, LineManagerAPI

urlpatterns = [
    path('add_leave_request/',LeaveRequestAPI.as_view(),name="add-leave-request"),
    path('get_leave_request/',LineManagerAPI.as_view(),name="get-leave-request"),
]
