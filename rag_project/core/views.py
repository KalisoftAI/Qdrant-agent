# core/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from .rag_logic.chain import get_analysis_chain, CONVERSATION_STAGES
from appointments.models import Appointment, DoctorNote # DoctorNote imported
from .models import ChatSession # ChatSession imported
from accounts.models import User
from doctor_tools.models import DoctorQuery
@login_required
def index(request):
    doctors_notes = DoctorNote.objects.filter(patient=request.user).order_by('-created_at')
    doctor_summaries = DoctorQuery.objects.filter(patient=request.user).order_by('-created_at')
    
    request.session['chat_history'] = []
    request.session['conversation_stage'] = 'GET_INITIAL_PROBLEM'
    
    context = {
        'doctors_notes': doctors_notes,
        'doctor_summaries': doctor_summaries,
    }
    return render(request, 'core/index.html', context)

@login_required
def chat(request):
    """
    Handles the chat, and saves the session to the database upon completion.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    body = json.loads(request.body.decode('utf-8'))
    user_message = body.get('question', '')
    chat_history = request.session.get('chat_history', [])
    current_stage = request.session.get('conversation_stage', 'GET_INITIAL_PROBLEM')
    
    if user_message:
        chat_history.append({'speaker': 'Patient', 'line': user_message})
    
    next_stage_key = CONVERSATION_STAGES.get(current_stage, {}).get('next_stage')
    
    bot_response = ""
    is_complete = False
    follow_up_action = None

    if next_stage_key == 'ANALYZE':
        is_complete = True
        formatted_history = "\n".join([f"{turn['speaker']}: {turn['line']}" for turn in chat_history])
        analysis_chain = get_analysis_chain()
        final_analysis = analysis_chain.invoke({'chat_history': formatted_history}).strip()
        
        if final_analysis.startswith('[CONCLUSION: MAJOR]'):
            follow_up_action = {
                "type": "ask_to_book",
                "question": "Would you like me to help you book an appointment with a nearby hospital?",
                "options": [{"text": "Yes", "payload": "wants_to_book"}, {"text": "No", "payload": "does_not_want_to_book"}]
            }
            bot_response = final_analysis.replace('[CONCLUSION: MAJOR]', '').strip()
        else:
            bot_response = final_analysis.replace('[CONCLUSION: MINOR]', '').strip()

        chat_history.append({'speaker': 'AI Agent', 'line': bot_response})
        request.session['conversation_stage'] = 'COMPLETE'

        # When the conversation is complete, save it.
        ChatSession.objects.create(
            patient=request.user,
            transcript=chat_history
        )

    elif next_stage_key:
        is_complete = False
        stage_info = CONVERSATION_STAGES[next_stage_key]
        bot_response = stage_info['prompt']
        chat_history.append({'speaker': 'AI Agent', 'line': bot_response})
        request.session['conversation_stage'] = next_stage_key
    else:
        is_complete = True
        bot_response = "Our screening is complete. Please click 'Start Over' to begin a new conversation."

    request.session['chat_history'] = chat_history
    return JsonResponse({
        'answer': bot_response, 
        'is_complete': is_complete, 
        'follow_up_action': follow_up_action
    })

@login_required
def get_patient_appointments_api(request):
    appointments = Appointment.objects.filter(patient=request.user).order_by('-created_at')
    data = [{
        'hospital': app.requested_hospital_name,
        'status': app.get_status_display(),
        'date': app.appointment_date,
        'time': app.appointment_time,
        'doctor': f"{app.doctor.first_name} {app.doctor.last_name}" if app.doctor else None
    } for app in appointments]
    return JsonResponse({'appointments': data})

@login_required
def reset_chat(request):
    request.session['chat_history'] = []
    request.session['conversation_stage'] = 'GET_INITIAL_PROBLEM'
    initial_prompt = "Hello! I am a specialized AI agent for diabetes screening. To start, could you please tell me about the main problem or symptoms you are experiencing?"
    return JsonResponse({'answer': initial_prompt})

@login_required
def doctor_dashboard(request):
    if request.user.role != 'DOCTOR':
        return redirect('index') 
    return redirect('doctor_tools:dashboard')