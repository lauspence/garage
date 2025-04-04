# forms.py
from django import forms
from .models import InsurancePolicy, InsuranceClaim

class InsurancePolicyForm(forms.ModelForm):
    class Meta:
        model = InsurancePolicy
        fields = ['vehicle', 'policy_number', 'provider', 'coverage_type', 'start_date', 'end_date', 'premium_amount', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class InsuranceClaimForm(forms.ModelForm):
    class Meta:
        model = InsuranceClaim
        fields = ['policy', 'claim_number', 'date_of_incident', 'description', 'claim_amount', 'status']
        widgets = {
            'date_of_incident': forms.DateInput(attrs={'type': 'date'}),
        }
