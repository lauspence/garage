from django.contrib import admin
from .models import CustomUser  # Import your CustomUser model

# ✅ CustomUser Model Admin
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active')  # You can filter by role, is_staff, etc.
    search_fields = ('username', 'email')  # Allows searching by username and email
    readonly_fields = ('date_joined',)  # Date joined is a read-only field

# Register the CustomUser model with the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
