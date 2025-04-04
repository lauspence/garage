from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *

def insurance_home(request):
    insurance_policies = InsurancePolicy.objects.all()
    return render(request, 'insurance/home.html', {'insurance_policies': insurance_policies})

def view_insurance_policies(request):
    policies = InsurancePolicy.objects.all()
    return render(request, 'insurance/view_policies.html', {'policies': policies})


def add_insurance_policy(request):
    if request.method == 'POST':
        form = InsurancePolicyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_insurance_policies')
    else:
        form = InsurancePolicyForm()
    return render(request, 'insurance/add_policy.html', {'form': form})


def file_insurance_claim(request):
    if request.method == 'POST':
        form = InsuranceClaimForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_insurance_policies')  # Redirect back to policies or a claim success page
    else:
        form = InsuranceClaimForm()
    return render(request, 'insurance/file_claim.html', {'form': form})


def update_insurance_policy(request, policy_id):
    policy = get_object_or_404(InsurancePolicy, id=policy_id)
    if request.method == 'POST':
        form = InsurancePolicyForm(request.POST, instance=policy)
        if form.is_valid():
            form.save()
            return redirect('view_insurance_policies')
    else:
        form = InsurancePolicyForm(instance=policy)
    return render(request, 'insurance/update_policy.html', {'form': form, 'policy': policy})


def delete_insurance_policy(request, policy_id):
    policy = get_object_or_404(InsurancePolicy, id=policy_id)
    if request.method == 'POST':
        policy.delete()
        return redirect('view_insurance_policies')
    return render(request, 'insurance/delete_policy.html', {'policy': policy})