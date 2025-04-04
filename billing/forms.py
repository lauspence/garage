from django import forms
from .models import *
from django.contrib import admin

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'registration_number']

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['service', 'part', 'part_quantity', 'payment_method', 'payment_amount']

    service = forms.ModelChoiceField(queryset=Service.objects.all(), required=False)
    part = forms.ModelChoiceField(queryset=Part.objects.all(), required=False)


class EstimateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = ['customer', 'vehicle', 'status'] 

class EstimateItemForm(forms.ModelForm):
    class Meta:
        model = EstimateItem
        fields = ["part_name", "quantity", "unit_price"]

class VehicleEstimateRequestForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['registration_number', 'make', 'model', 'year', 'color', 'insurance_company']  # Include 'make' here
    
    parts = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'List parts needed, e.g., Side Mirror - 2'}), required=True, label="Requested Parts")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['color'].required = True
        self.fields['insurance_company'].required = True

    def clean_parts(self):
        parts_text = self.cleaned_data.get('parts')
        # Validate parts format (e.g., "Part Name - Quantity")
        parts_list = parts_text.split('\n')
        for part in parts_list:
            if '-' not in part:
                raise forms.ValidationError("Each part must be in the format 'Part Name - Quantity'")
        return parts_text


class EstimateAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "vehicle", "created_at", "status")
    list_filter = ("status", "created_at")
    search_fields = ("customer__name", "vehicle__registration_number")
    ordering = ("-created_at",)
    actions = ["approve_estimate", "reject_estimate"]

    def approve_estimate(self, request, queryset):
        queryset.update(status="Approved")
        self.message_user(request, "Selected estimates have been approved.")

    def reject_estimate(self, request, queryset):
        queryset.update(status="Rejected")
        self.message_user(request, "Selected estimates have been rejected.")

    approve_estimate.short_description = "Approve selected estimates"
    reject_estimate.short_description = "Reject selected estimates"
