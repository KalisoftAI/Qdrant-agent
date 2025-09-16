# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, PatientProfile, DoctorProfile

class PatientSignUpForm(UserCreationForm):
    # Fields from PatientProfile model
    age = forms.IntegerField(required=True)
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], required=True)
    mobile_no = forms.CharField(max_length=15, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.PATIENT
        user.save()
        PatientProfile.objects.create(
            user=user,
            age=self.cleaned_data.get('age'),
            gender=self.cleaned_data.get('gender'),
            mobile_no=self.cleaned_data.get('mobile_no')
        )
        return user

class DoctorSignUpForm(UserCreationForm):
    # Fields from DoctorProfile model
    hospital_name = forms.CharField(max_length=255, required=True)
    qualification = forms.CharField(max_length=255, required=True)
    mobile_no = forms.CharField(max_length=15, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.DOCTOR
        user.save()
        DoctorProfile.objects.create(
            user=user,
            hospital_name=self.cleaned_data.get('hospital_name'),
            qualification=self.cleaned_data.get('qualification'),
            mobile_no=self.cleaned_data.get('mobile_no')
        )
        return user