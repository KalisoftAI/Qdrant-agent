# doctor_tools/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
import nest_asyncio

from .rag_logic.chain import get_doctor_rag_chain
from appointments.models import Appointment, DoctorNote
from accounts.models import User
from core.models import ChatSession
from .models import DoctorQuery

from langchain_google_genai import ChatGoogleGenerativeAI
from doctor_tools.rag_logic import rag_config

def is_doctor(user):
    return user.is_authenticated and user.role == 'DOCTOR'

@login_required
def dashboard_view(request):
    if not is_doctor(request.user):
        return redirect('index')
    
    all_patients = User.objects.filter(role=User.Role.PATIENT)
    pending_appointments = Appointment.objects.filter(status=Appointment.Status.PENDING).order_by('created_at')
    confirmed_appointments = Appointment.objects.filter(doctor=request.user, status=Appointment.Status.CONFIRMED).order_by('-appointment_date', '-appointment_time')

    context = {
        'all_patients': all_patients,
        'pending_appointments': pending_appointments,
        'confirmed_appointments': confirmed_appointments,
    }
    return render(request, 'doctor_tools/dashboard.html', context)

@login_required
def patient_detail_view(request, patient_id):
    if not is_doctor(request.user):
        return redirect('index')

    patient = get_object_or_404(User, id=patient_id, role=User.Role.PATIENT)
    
    if request.method == 'POST':
        note_text = request.POST.get('note')
        if note_text:
            DoctorNote.objects.create(
                patient=patient,
                doctor=request.user,
                note=note_text
            )
        return redirect('doctor_tools:patient_detail', patient_id=patient.id)

    chat_sessions = ChatSession.objects.filter(patient=patient).order_by('-created_at')
    doctors_notes = DoctorNote.objects.filter(patient=patient).order_by('-created_at')
    
    context = {
        'patient': patient,
        'chat_sessions': chat_sessions,
        'doctors_notes': doctors_notes,
    }
    return render(request, 'doctor_tools/patient_detail.html', context)

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

@login_required
def ask_question_api(request):
    if not is_doctor(request.user):
        return JsonResponse({'error': 'Forbidden'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
    try:
        body = json.loads(request.body)
        question = body.get('question', '')
        patient_id = body.get('patient_id')

        if not question or not patient_id:
            return JsonResponse({'error': 'Question and Patient ID are required'}, status=400)
        
        patient = get_object_or_404(User, id=patient_id)
        chain = get_or_initialize_chain()
        if not chain:
            return JsonResponse({'error': 'RAG chain is not available'}, status=500)

        raw_answer = chain.invoke(question)

        summary_prompt = f"""
        You are a helpful assistant. Please summarize the following clinical analysis for a patient in 2-3 simple, clear, and encouraging sentences. Avoid complex medical jargon.
        
        Clinical Analysis:
        "{raw_answer}"
        
        Simplified Summary for Patient:
        """
        llm = ChatGoogleGenerativeAI(model=rag_config.LLM_MODEL, temperature=0.2, google_api_key=rag_config.GOOGLE_API_KEY)
        patient_summary = llm.invoke(summary_prompt).content

        DoctorQuery.objects.create(
            doctor=request.user,
            patient=patient,
            query_text=question,
            raw_response=raw_answer,
            patient_summary=patient_summary
        )

        return JsonResponse({'answer': raw_answer})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)