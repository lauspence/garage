from django.urls import path
from .views import *

app_name = "services"  # ✅ This must be defined

urlpatterns = [
    path('', services_home, name='services'),  
    path('list/', service_list, name='service_list'),
    path("request/", request_service, name="request_service"),
    path("request_success/", request_success, name="request_success"),
    path("track/", track_service_progress, name="track_service_progress"),
    path("booking/<int:booking_id>/", booking_detail, name="booking_detail"),




]
