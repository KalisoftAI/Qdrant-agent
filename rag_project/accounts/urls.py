# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_selection, PatientSignUpView, DoctorSignUpView

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register_selection, name='register_selection'),
    path('register/patient/', PatientSignUpView.as_view(), name='patient_register'),
    path('register/doctor/', DoctorSignUpView.as_view(), name='doctor_register'),
]