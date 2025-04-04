from django.urls import path
from .views import vehicles_home

urlpatterns = [
    path('', vehicles_home, name='vehicles_home'),
]
