from django.urls import path
from .views import *

urlpatterns = [
    path('', billing_home, name='billing'),
    path('create_customer/',create_customer, name='create_customer'),
    path('create_vehicle/<int:customer_id>/', create_vehicle, name='create_vehicle'),
    path('create_booking/<int:vehicle_id>/', create_booking, name='create_booking'),
    path('create_billing/<int:booking_id>/', create_billing, name='create_billing'),
    path('generate_invoice/<int:billing_id>/', generate_invoice, name='generate_invoice'),
    path('payment/', make_payment, name='make_payment'),
    path("process-payment/", process_payment, name="process_payment"),
    path("estimates/create/", create_estimate, name="create_estimate"),
    path("estimates/", view_estimates, name="view_estimates"),
    path('estimates/<int:id>/', estimate_detail, name='estimate_detail'),
    path('request-estimate/', request_estimate, name='request_estimate'),
]
