from django.contrib import admin
from .models import Booking, Service

# ✅ Booking Model Admin
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'status', 'date')  
    list_filter = ('service', 'status')  
    search_fields = ('name', 'email', 'service__name')  # 🔥 Fixed ForeignKey search
    readonly_fields = ('created_at',)  

# ✅ Service Model Admin
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'estimated_time', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)

# Register models
admin.site.register(Booking, BookingAdmin)
admin.site.register(Service, ServiceAdmin)
