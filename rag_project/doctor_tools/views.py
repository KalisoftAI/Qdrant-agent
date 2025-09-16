# doctor_tools/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
import nest_asyncio
from .rag_logic.chain import get_doctor_rag_chain
from appointments.models import Appointment

doctor_rag_chain = None

def get_or_initialize_chain():
    global doctor_rag_chain
    if doctor_rag_chain is None:
        nest_asyncio.apply()
        try:
            print("🚀 Initializing Doctor's RAG chain...")
            doctor_rag_chain = get_doctor_rag_chain()
            print("✅ Doctor's RAG chain ready.")
        except Exception as e:
            print(f"❌ Error initializing Doctor's RAG chain: {e}")
            raise e
    return doctor_rag_chain

def is_doctor(user):
    return user.is_authenticated and user.role == 'DOCTOR'

@login_required
def dashboard_view(request):
    if not is_doctor(request.user):
        return redirect('index')
    
    pending_appointments = Appointment.objects.filter(status=Appointment.Status.PENDING).order_by('created_at')
    confirmed_appointments = Appointment.objects.filter(doctor=request.user, status=Appointment.Status.CONFIRMED).order_by('-appointment_date', '-appointment_time')

    context = {
        'pending_appointments': pending_appointments,
        'confirmed_appointments': confirmed_appointments,
    }
    return render(request, 'doctor_tools/dashboard.html', context)

@login_required
def ask_question_api(request):
    if not is_doctor(request.user):
        return JsonResponse({'error': 'Forbidden'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    try:
        chain = get_or_initialize_chain()
        if not chain:
            return JsonResponse({'error': 'RAG chain is not available'}, status=500)
        body = json.loads(request.body)
        question = body.get('question', '')
        if not question:
            return JsonResponse({'error': 'Question is required'}, status=400)
        answer = chain.invoke(question)
        return JsonResponse({'answer': answer})
    except Exception as e:
        print(f"API Error: {e}")
        return JsonResponse({'error': str(e)}, status=500)