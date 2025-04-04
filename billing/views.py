import uuid
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponseRedirect
from datetime import datetime
from django.utils import timezone
from django.urls import reverse
from .models import *
from .forms import *


def is_admin(user):
    return user.is_staff or user.role == "admin"


def billing_home(request):
    return render(request, "billing/home.html")


@login_required
def create_customer(request):
    """Creates or updates a customer profile linked to the logged-in user."""
    customer, created = Customer.objects.get_or_create(
        user=request.user,
        defaults={"name": request.user.username, "email": request.user.email},
    )

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()

            # Fetch the latest vehicle (if exists), else redirect to vehicle creation
            latest_vehicle = customer.vehicle_set.first()  # Assuming One-to-Many (Customer → Vehicles)
            if latest_vehicle:
                return redirect("create_booking", vehicle_id=latest_vehicle.id)
            else:
                return redirect("create_vehicle", customer_id=customer.id)  # Adjust this URL if needed

    else:
        form = CustomerForm(instance=customer)

    return render(request, "billing/create_customer.html", {"form": form, "customer": customer})

@login_required
def create_vehicle(request, customer_id):
    """Allows a customer to add a vehicle to their profile."""
    customer = get_object_or_404(Customer, id=customer_id, user=request.user)

    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.customer = customer  # Associate the vehicle with the customer
            vehicle.save()

            # Redirect to the create_booking page with the newly added vehicle
            return redirect("create_booking", vehicle_id=vehicle.id)
    else:
        form = VehicleForm()

    return render(request, "billing/create_vehicle.html", {"form": form, "customer": customer})



@login_required
def create_booking(request, vehicle_id):
    """Allows a customer to book a service for their vehicle."""
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == "POST":
        service_id = request.POST.get("service")
        selected_service = get_object_or_404(Service, id=service_id)

        # Create a new booking
        booking = Booking.objects.create(
            user=request.user, vehicle=vehicle, service=selected_service
        )

        # Generate a billing entry automatically
        Billing.objects.create(
            booking=booking,
            total_cost=selected_service.cost,
            payment_method="",
            payment_amount=0,
        )

        return redirect("create_billing", booking_id=booking.id)

    return render(
        request,
        "billing/create_booking.html",
        {"vehicle": vehicle, "services": Service.objects.all()},
    )


@login_required
def create_billing(request, booking_id):
    """Generates a billing record after a booking is made."""
    booking = get_object_or_404(Booking, id=booking_id)

    # Get the booked service and other details
    booked_service = booking.service
    vehicle = booking.vehicle  # Get the vehicle associated with the booking
    parts = Part.objects.all()

    print(f"Debug - Booking ID: {booking.id}, Service: {booked_service.name} - KSH {booked_service.cost}")

    if request.method == "POST":
        part_id = request.POST.get("part")
        selected_part = Part.objects.get(id=part_id) if part_id else None
        payment_method = request.POST.get("payment_method")
        payment_amount = float(request.POST.get("payment_amount", 0))

        # Calculate total cost
        total_cost = booked_service.cost + (selected_part.cost if selected_part else 0)

        billing, created = Billing.objects.update_or_create(
            booking=booking,
            defaults={
                "part": selected_part,
                "payment_method": payment_method,
                "payment_amount": payment_amount,
                "total_cost": total_cost,
            },
        )

        return redirect("generate_invoice", billing_id=billing.id)

    return render(
        request,
        "billing/create_billing.html",
        {
            "vehicle": vehicle,
            "booked_service": booked_service,
            "parts": parts,
        },
    )




def generate_invoice_number():
    """Generates a unique invoice number in the format INV-YYYYMMDD-XXX."""
    today = datetime.today().strftime("%Y%m%d")
    last_invoice = Invoice.objects.filter(invoice_number__startswith=f"INV-{today}").order_by("-invoice_number").first()

    new_number = (int(last_invoice.invoice_number.split("-")[-1]) + 1) if last_invoice else 1
    return f"INV-{today}-{new_number:03d}"


def generate_invoice(request, billing_id):
    # Get the Billing object, or return 404 if not found
    billing = get_object_or_404(Billing, id=billing_id)

    try:
        # Attempt to access the related Invoice
        invoice = billing.invoice
    except Invoice.DoesNotExist:
        # If the Invoice does not exist, create one
        invoice_number = generate_invoice_number()  # Generate a unique invoice number
        invoice = Invoice.objects.create(
            billing=billing,
            invoice_number=invoice_number,
            total_amount=billing.total_cost,
            date_created=timezone.now(),
        )

    return render(request, "billing/invoice.html", {"invoice": invoice, "billing": billing})


def make_payment(request):
    # Fetch the latest booking of the logged-in user
    last_booking = Booking.objects.filter(user=request.user).order_by('-created_at').first()

    if last_booking:
        service = last_booking.service.name  # Get service name
        amount = last_booking.service.cost  # Get service cost
    else:
        service = "Unknown Service"
        amount = 5000  # Default amount if no booking found

    return render(request, "billing/make_payment.html", {
        "service": service,
        "amount": amount
    })

def process_payment(request):
    if request.method == "POST":
        service = request.POST.get("service")
        amount = request.POST.get("amount")

        # Here, you can integrate MPesa, Stripe, PayPal, etc.
        return render(request, "billing/payment_success.html", {
            "service": service,
            "amount": amount
        })

    return HttpResponseRedirect(reverse("booking"))



@user_passes_test(lambda user: user.is_superuser)
@login_required
def create_estimate(request):
    if request.method == "POST":
        estimate_form = EstimateForm(request.POST)
        item_form = EstimateItemForm(request.POST)

        if estimate_form.is_valid() and item_form.is_valid():
            # Save the estimate
            estimate = estimate_form.save(commit=False)
            estimate.customer = request.user  # Admin creates the estimate, not the regular user
            estimate.save()

            # Create the estimate items and link them to the estimate
            item = item_form.save(commit=False)
            item.estimate = estimate
            item.save()

            return redirect('view_estimates')  # Redirect to view all estimates

    else:
        estimate_form = EstimateForm()
        item_form = EstimateItemForm()

    return render(request, "billing/create_estimate.html", {
        "estimate_form": estimate_form,
        "item_form": item_form
    })

@login_required
def request_estimate(request):
    if request.method == "POST":
        form = VehicleEstimateRequestForm(request.POST)
        if form.is_valid():
            # Get the CustomUser instance for the logged-in user
            user = request.user
            
            # Get or create the Customer instance (if it's linked to the CustomUser)
            customer, created = Customer.objects.get_or_create(user=user)
            
            # Get vehicle details from the form
            registration_number = form.cleaned_data['registration_number']
            
            # Check if vehicle already exists with this registration number
            vehicle, vehicle_created = Vehicle.objects.get_or_create(
                registration_number=registration_number,
                defaults={
                    'customer': customer,  # Link to the Customer, which links to the CustomUser
                    'make': form.cleaned_data['make'],
                    'model': form.cleaned_data['model'],
                    'year': form.cleaned_data['year'],
                    'color': form.cleaned_data['color'],
                    'insurance_company': form.cleaned_data['insurance_company'],
                }
            )
            
            # Now create the estimate and assign the user (CustomUser) and vehicle
            estimate = Estimate.objects.create(
                customer=user,  # Assign the CustomUser instance here, not the Customer
                vehicle=vehicle,
            )
            
            # Save requested parts (including unit prices)
            parts_text = form.cleaned_data['parts']
            parts_list = parts_text.split('\n')

            for part in parts_list:
                if '-' in part:
                    part_name, quantity = part.split('-')
                    quantity = int(quantity.strip())  # Ensure the quantity is an integer
                    unit_price = form.cleaned_data.get('unit_price', 0)  # Default unit price if not provided
                    EstimateItem.objects.create(
                        estimate=estimate,
                        part_name=part_name.strip(),
                        quantity=quantity,
                        unit_price=unit_price  # Ensure unit price is passed
                    )

            messages.success(request, "✅ Estimate request submitted successfully!")
            return redirect('view_estimates')  # Check if redirect is correct
    else:
        form = VehicleEstimateRequestForm()

    return render(request, 'billing/request_estimate.html', {'form': form})


@login_required
def view_estimates(request):
    if request.user.is_superuser:
        # Admin can view all estimates
        estimates = Estimate.objects.all()
    else:
        # Regular users can only view estimates associated with their own vehicles
        estimates = Estimate.objects.filter(vehicle__customer__user=request.user)  # Assuming vehicle has a user relation
    
    return render(request, "billing/view_estimates.html", {
        'estimates': estimates
    })

def estimate_detail(request, id):
    estimate = get_object_or_404(Estimate, id=id)
    return render(request, 'billing/estimate_detail.html', {'estimate': estimate})





