# models.py
from django.db import models

class Vehicle(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vin = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.make} {self.model} ({self.year})'


class InsurancePolicy(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    policy_number = models.CharField(max_length=50, unique=True)
    provider = models.CharField(max_length=100)
    coverage_type = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.policy_number} ({self.vehicle.make} {self.vehicle.model})'


class InsuranceClaim(models.Model):
    policy = models.ForeignKey(InsurancePolicy, on_delete=models.CASCADE)
    claim_number = models.CharField(max_length=50, unique=True)
    date_of_incident = models.DateField()
    description = models.TextField()
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])

    def __str__(self):
        return f'Claim #{self.claim_number} for {self.policy.policy_number}'
