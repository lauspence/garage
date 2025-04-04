from django.db import models
from accounts.models import CustomUser

class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    registration_number = models.CharField(max_length=20, unique=True)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=50, default="Unknown")
    insurance_company = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.make} {self.model} - {self.registration_number}"

class Service(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - KSH {self.cost}"

class Part(models.Model):
    name = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - KSH {self.cost}"

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,  related_name="customer_bookings",null=True,blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="bookings")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="bookings" )
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of booking

    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.service.name}"

class Billing(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, null=True, blank=True, related_name="billings")
    part = models.ForeignKey(Part, on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings")
    part_quantity = models.IntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Ensuring no NULL values
    payment_method = models.CharField(max_length=50)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_total(self):
        total = self.booking.service.cost if self.booking else 0  # Prevents crashes if booking is NULL
        if self.part:
            total += self.part.cost * self.part_quantity
        return total

    def save(self, *args, **kwargs):
        self.total_cost = self.calculate_total()  # Ensure total cost is always set
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Billing for {self.booking} - Total: KSH {self.total_cost}"
    
class Invoice(models.Model):
    billing = models.OneToOneField(Billing, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=50, unique=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')], default='Unpaid')

    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.payment_status}"

    def generate_invoice_number(self):
        # Generates a unique invoice number based on the ID and date
        return f"INV-{self.id}"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            super().save(*args, **kwargs)  # Save first to get a PK
            self.invoice_number = self.generate_invoice_number()
        self.total_amount = self.billing.total_cost  # Ensure total amount is copied
        super().save(*args, **kwargs)  # Save again with invoice number

class Estimate(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="estimates", default=None)
    vehicle = models.ForeignKey("Vehicle", on_delete=models.CASCADE, related_name="estimates", default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")],
        default="Pending"
    )

    def __str__(self):
        return f"Estimate for {self.vehicle.registration_number} - {self.status}"



class EstimateItem(models.Model):
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE, related_name="items")
    part_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    def __str__(self):
        return f"{self.part_name} (x{self.quantity}) - KSH {self.total_price}"

