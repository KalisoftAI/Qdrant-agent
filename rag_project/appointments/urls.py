# appointments/urls.py
from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('api/find-hospitals/', views.find_hospitals_api, name='find_hospitals'),
    path('api/request/', views.create_appointment_request_api, name='create_request'),
    path('api/confirm/<int:pk>/', views.confirm_appointment_api, name='confirm'),
]