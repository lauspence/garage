from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('booking/', booking_view, name='booking'),
    path('manage/bookings/', admin_bookings, name='admin_bookings'),
    path('manage/bookings/approve/<int:booking_id>/', approve_booking, name='approve_booking'),
    path('manage/bookings/cancel/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    # path('assign_mechanic/<int:booking_id>/', assign_mechanic, name='assign_mechanic'),
    path('update_booking_status/<int:booking_id>/', update_booking_status, name='update_booking_status'),
    path('mechanic/dashboard/', mechanic_dashboard, name='mechanic_dashboard'),
    path('services/', service_list, name='service_list'),
    path('bookings/', booking_list, name='booking_list'),

    
]
