# accounts/views.py
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import PatientSignUpForm, DoctorSignUpForm

class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'accounts/patient_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'patient'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class DoctorSignUpView(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = 'accounts/doctor_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'doctor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        # --- THIS IS THE FIX ---
        # Redirect doctors to their new dashboard after registration
        return redirect('doctor_tools:dashboard')


def register_selection(request):
    return render(request, 'accounts/register_selection.html')


@login_required
def login_redirect_view(request):
    if request.user.role == 'DOCTOR':
        return redirect('doctor_tools:dashboard')
    elif request.user.role == 'PATIENT':
        return redirect('index')
    else:
        return redirect('accounts:login')