from django import forms
from billing.models import Booking, Vehicle, Service

class ServiceRequestForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(),  # Fetch services dynamically
        empty_label="Select a service",
        widget=forms.Select(attrs={'class': 'form-control'})  # Bootstrap styling
    )

    vehicle = forms.ModelChoiceField(
        queryset=Vehicle.objects.none(),  # Will be set dynamically in __init__
        empty_label="Select your vehicle",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Preferred Date"
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )

    class Meta:
        model = Booking
        fields = ['service', 'vehicle', 'date', 'message']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(customer=user.customer)  # Fetch user's vehicles
