# accounts/models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model supporting email as the unique identifier.
    """
    class Role(models.TextChoices):
        DOCTOR = "DOCTOR", "Doctor"
        PATIENT = "PATIENT", "Patient"

    # We don't need a username, email will be the unique identifier
    username = None
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=50, choices=Role.choices)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    patient_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    mobile_no = models.CharField(max_length=15)

    def __str__(self):
        return f"Patient: {self.user.first_name} {self.user.last_name}"

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    hospital_name = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=15)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"