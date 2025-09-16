# core/models.py
from django.db import models
from django.conf import settings

class ChatSession(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_sessions')
    transcript = models.JSONField() # Store the list of chat messages
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat session for {self.patient.email} on {self.created_at.strftime('%Y-%m-%d')}"