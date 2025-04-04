from django.shortcuts import render, redirect ,get_object_or_404
from core.models import *
from django.contrib.auth.decorators import login_required
from billing.models import Booking, Vehicle 
from .forms import ServiceRequestForm

def services_home(request):
    services = Service.objects.all()  # Fetch services from DB
    return render(request, 'services/home.html', {'services': services})

def service_list(request):
    services = [
        {
            "name": "Oil Change",
            "description": "Keep your engine running smoothly with our premium oil change service.",
            "price": "Ksh 6,500",
            "image": "images/oil_change.png",
        },
        {
            "name": "Car Diagnostics",
            "description": "Advanced vehicle diagnostics to detect and resolve issues quickly.",
            "price": "Ksh 9,100",
            "image": "images/diagnostics.jpg",
        },
        {
            "name": "Brake Repair",
            "description": "Ensure your safety with professional brake repair and replacement services.",
            "price": "Ksh 13,000",
            "image": "images/brake_repair.jpg",
        },
        {
            "name": "Battery Replacement",
            "description": "Fast and reliable battery testing and replacement services.",
            "price": "Ksh 10,400",
            "image": "images/battery_replacement.jpg",
        },
        {
            "name": "Tire Rotation & Balancing",
            "description": "Extend the life of your tires with proper rotation and balancing.",
            "price": "Ksh 7,800",
            "image": "images/tire_rotation.jpg",
        },
        {
            "name": "Full Car Service",
            "description": "Comprehensive maintenance to keep your car in peak condition.",
            "price": "Ksh 26,000",
            "image": "images/full_service.jpg",
        },
    ]

    return render(request, 'services/service_list.html', {'services': services})

@login_required
def request_service(request):
    user = request.user  # Get the logged-in user

    if request.method == "POST":
        form = ServiceRequestForm(request.POST, user=user)  # Pass the form data
        if form.is_valid():
            service = form.cleaned_data["service"]
            vehicle = form.cleaned_data["vehicle"]

            # ✅ Create a booking (without date and message)
            Booking.objects.create(
                user=user,
                vehicle=vehicle,
                service=service
            )
            return redirect("services:request_success")  # Redirect after successful booking
    else:
        form = ServiceRequestForm()  # If not POST, initialize an empty form

    return render(request, "services/request_service.html", {"form": form})

def request_success(request):
    return render(request, "services/request_success.html")

def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "services/booking_detail.html", {"booking": booking})


def track_service_progress(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-created_at")  # Fetch user's bookings
    return render(request, "services/track_service.html", {"bookings": bookings})
