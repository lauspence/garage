from django.conf import settings
from django.db import models



class Booking(models.Model):
    SERVICE_CHOICES = [
        ('oil_change', 'Oil Change'),
        ('brake_check', 'Brake Check'),
        ('tire_replacement', 'Tire Replacement'),
        ('engine_diagnosis', 'Engine Diagnosis'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    date = models.DateField()
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='pending')

    mechanic = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,null=True, blank=True, related_name="mechanic_bookings")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service} on {self.date}"
    
class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    estimated_time = models.DurationField(help_text="Estimated completion time")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

