from django.urls import path
from .views import *

urlpatterns = [
    path('', insurance_home, name='insurance'),
    path('policies/', view_insurance_policies, name='view_insurance_policies'),
    path('policy/add/', add_insurance_policy, name='add_insurance_policy'),
    path('claim/file/', file_insurance_claim, name='file_insurance_claim'),
    path('update/<int:policy_id>/', update_insurance_policy, name='update_insurance_policy'),
    path('policy/delete/<int:policy_id>/', delete_insurance_policy, name='delete_insurance_policy'),
]
