# doctor_tools/urls.py
from django.urls import path
from . import views

app_name = 'doctor_tools'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('api/ask/', views.ask_question_api, name='ask_api'),
]