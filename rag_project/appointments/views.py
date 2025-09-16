# appointments/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .models import Appointment
from .utils import find_hospitals
from accounts.models import User

@login_required
def find_hospitals_api(request):
    location = request.GET.get('location')
    if not location:
        return JsonResponse({'error': 'Location is required.'}, status=400)
    try:
        hospitals = find_hospitals(location)
        return JsonResponse({'hospitals': hospitals})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def create_appointment_request_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    if request.user.role != User.Role.PATIENT:
        return JsonResponse({'error': 'Forbidden'}, status=403)

    data = json.loads(request.body)
    Appointment.objects.create(
        patient=request.user,
        requested_hospital_name=data.get('name'),
        requested_hospital_address=data.get('address'),
        status=Appointment.Status.PENDING
    )
    return JsonResponse({'message': 'Appointment request sent successfully.'})

@login_required
def confirm_appointment_api(request, pk):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    if request.user.role != User.Role.DOCTOR:
        return JsonResponse({'error': 'Forbidden'}, status=403)
        
    appointment = get_object_or_404(Appointment, pk=pk)
    data = json.loads(request.body)
    
    appointment.doctor = request.user
    appointment.appointment_date = data.get('date')
    appointment.appointment_time = data.get('time')
    appointment.status = Appointment.Status.CONFIRMED
    appointment.save()
    
    return JsonResponse({'message': 'Appointment confirmed successfully.'})