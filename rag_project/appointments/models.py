# appointments/models.py
from django.db import models
from django.conf import settings

class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_appointments')
    
    requested_hospital_name = models.CharField(max_length=255)
    requested_hospital_address = models.TextField()
    
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    
    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment for {self.patient.first_name} at {self.requested_hospital_name} ({self.status})"

class DoctorNote(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes_for_patient')
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes_by_doctor')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.patient.first_name} by Dr. {self.doctor.first_name}"