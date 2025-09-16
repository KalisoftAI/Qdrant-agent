# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat, name='chat'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('reset-chat/', views.reset_chat, name='reset_chat'),
    path('api/my-appointments/', views.get_patient_appointments_api, name='my_appointments'),
]