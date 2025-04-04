from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.conf import settings
from accounts.models import CustomUser
from billing.models import Booking, Estimate
from .forms import *
from .models import *

# Create your views here.
def home(request):
    # Check if the user is part of the 'Mechanic' group
    is_mechanic = request.user.groups.filter(name='Mechanic').exists()
    return render(request, 'core/home.html', {'is_mechanic': is_mechanic})

# CustomUser = get_user_model()  # Ensure we use the custom user model

CustomUser = get_user_model()  # Get the Custom User model
@login_required
def admin_bookings(request):
    # Count bookings by status
    approved_count = Booking.objects.filter(status__iexact='approved').count()
    pending_count = Booking.objects.filter(status__iexact='pending').count()
    canceled_count = Booking.objects.filter(status__iexact='canceled').count()

    # Total registered users
    total_users = CustomUser.objects.count()

    # Fetch all bookings and mechanics
    bookings = Booking.objects.all().order_by('-created_at')
    mechanics = CustomUser.objects.filter(groups__name="Mechanic")

    # Fetch Pending Estimates
    pending_estimates = Estimate.objects.filter(status="Pending")

    if request.method == "POST":
        booking_id = request.POST.get('booking_id')
        mechanic_id = request.POST.get('mechanic_id')

        if not booking_id or not mechanic_id:
            messages.error(request, "❌ Please select a mechanic!")
            return redirect('admin_bookings')

        booking = get_object_or_404(Booking, id=booking_id)
        mechanic = get_object_or_404(CustomUser, id=mechanic_id)

        booking.mechanic = mechanic
        booking.status = 'approved'  # Automatically approve when assigning
        booking.save()

        messages.success(request, f"✅ {mechanic.get_full_name()} assigned to {booking.name}'s booking!")
        return redirect('admin_bookings')

    context = {
        'approved_count': approved_count,
        'pending_count': pending_count,
        'canceled_count': canceled_count,
        'total_users': total_users,
        'bookings': bookings,
        'mechanics': mechanics,
        'pending_estimates': pending_estimates,  # Include pending estimates
    }

    return render(request, 'core/admin_bookings.html', context)





def approve_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Approved'
    booking.save()
    return redirect('admin_bookings')

def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'Canceled'
    booking.save()
    return redirect('admin_bookings')


@login_required
def booking_view(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)  # Don't save yet
            booking.user = request.user  # Assign the logged-in user
            booking.save()
            messages.success(request, "✅ Your booking has been successfully submitted!")
            return redirect('booking')  # Redirect after successful booking
    else:
        form = BookingForm()

    return render(request, 'core/booking.html', {'form': form})


@login_required
def update_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.user != booking.mechanic:
        return redirect('booking_list')  # Prevent unauthorized access

    if request.method == 'POST':
        form = UpdateBookingStatusForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking_list')

    else:
        form = UpdateBookingStatusForm(instance=booking)

    return render(request, 'update_booking_status.html', {'form': form, 'booking': booking})


@login_required
def mechanic_dashboard(request):
    if not request.user.groups.filter(name='Mechanic').exists():
        return redirect('home')

    # Fetch bookings assigned to the logged-in mechanic
    assigned_bookings = Booking.objects.filter(mechanic=request.user)

    return render(request, 'core/mechanic_dashboard.html', {'assigned_bookings': assigned_bookings})



def service_list(request):
    services = Service.objects.all()
    return render(request, 'core/service_list.html', {'services': services})


@login_required
def booking_list(request):
    """Display a list of bookings for the logged-in mechanic."""
    bookings = Booking.objects.filter(mechanic=request.user).order_by('-date')  # Show only assigned jobs
    return render(request, 'core/booking_list.html', {'bookings': bookings})


