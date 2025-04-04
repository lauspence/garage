from django.shortcuts import render

def vehicles_home(request):
    return render(request, 'vehicles/home.html')
