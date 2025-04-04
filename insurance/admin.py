from django.contrib import admin
from .models import InsurancePolicy, InsuranceClaim, Vehicle

# Register your models here.
admin.site.register(InsurancePolicy)
admin.site.register(InsuranceClaim)
admin.site.register(Vehicle)
