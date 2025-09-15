# core/views.py
from django.shortcuts import render
from django.http import JsonResponse
import json
from .rag_logic.chain import get_rag_chain

# Initialize the RAG chain once when the server starts
# This is more efficient than reloading it on every request.
try:
    rag_chain = get_rag_chain()
    print("✅ RAG chain initialized successfully.")
except Exception as e:
    rag_chain = None
    print(f"❌ Error initializing RAG chain: {e}")

def index(request):
    """
    Renders the main chat page.
    """
    return render(request, 'core/index.html')

def chat(request):
    """
    Handles the chat API endpoint. Receives a question and returns an answer.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    if not rag_chain:
        return JsonResponse({'error': 'RAG chain is not available.'}, status=500)

    try:
        # Decode the request body
        body = json.loads(request.body.decode('utf-8'))
        question = body.get('question', '')

        if not question:
            return JsonResponse({'error': 'Question is required.'}, status=400)

        # Get the answer from the RAG chain
        answer = rag_chain.invoke(question)

        return JsonResponse({'answer': answer})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON in request body'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)