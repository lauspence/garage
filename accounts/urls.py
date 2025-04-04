from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.accounts_home, name='accounts_home'),
    # Explicitly define the login template
    path('login/', views.login_view, name='login'),

    # Use Django's built-in LogoutView instead of a custom one
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('register/', views.register_view, name='register'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    

]
