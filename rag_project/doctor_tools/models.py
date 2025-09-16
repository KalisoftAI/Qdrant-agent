# doctor_tools/models.py
from django.db import models
from django.conf import settings

class DoctorQuery(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_queries')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='queries_about_patient')
    query_text = models.TextField()
    raw_response = models.TextField() # The full, detailed response for the doctor
    patient_summary = models.TextField() # The simplified summary for the patient
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query by Dr. {self.doctor.first_name} about {self.patient.first_name}"