from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(Vehicle)
admin.site.register(Service)
admin.site.register(Part)
admin.site.register(Billing)
admin.site.register(Booking)
admin.site.register(Invoice)
admin.site.register(Estimate)
admin.site.register(EstimateItem)
