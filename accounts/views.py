from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

def accounts_home(request):
    return render(request, 'accounts/home.html')  # Ensure this template exists

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # After successful registration, redirect to login page
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect based on role
            if user.is_staff:  # Admin users
                return redirect('admin_bookings')  # Redirect to Manage Bookings
            elif user.groups.filter(name='Mechanic').exists():  # Mechanic users
                return redirect('mechanic_dashboard')
            else:  # Default for customers
                return redirect('customer_dashboard')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password'})

    return render(request, 'accounts/login.html')

@login_required
def customer_dashboard(request):
    if request.user.is_staff:  # Prevent admins from accessing
        return HttpResponseForbidden("You are not allowed to access this page.")

    return render(request, 'accounts/customer_dashboard.html')
