# rag_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('doctor/', include('doctor_tools.urls')),
    path('appointments/', include('appointments.urls')), # Added
    path('', include('core.urls')),
]