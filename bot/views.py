# bot/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
import json
import uuid
from .models import ChatHistory, Doctor, Hospital

# Initialize chatbot predictor
bot_predictor = None

try:
    from .ml_model.chatbot_predictor import ChatbotPredictor
    bot_predictor = ChatbotPredictor()
    print("✅ Chatbot model loaded successfully!")
except Exception as e:
    print(f"⚠️ Warning: Chatbot model not loaded: {e}")
    print("   Please train the model first: python bot/ml_model/train_model.py")


def home_view(request):
    """Home page view"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {
        'user': request.user,
    }
    return render(request, 'bot/home.html', context)


@login_required
def chat_view(request):
    """Chat interface view"""
    # Get or create session ID
    session_id = request.session.get('chat_session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session['chat_session_id'] = session_id
    
    # Get chat history for current session
    chat_history = ChatHistory.objects.filter(
        user=request.user,
        session_id=session_id
    ).order_by('timestamp')[:50]
    
    context = {
        'chat_history': chat_history,
        'session_id': session_id
    }
    return render(request, 'bot/chat.html', context)


@login_required
@csrf_exempt
def send_message(request):
    """Handle chat messages via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('message', '').strip()
            
            if not question:
                return JsonResponse({
                    'success': False,
                    'error': 'Message cannot be empty'
                })
            
            # Check if model is loaded
            if bot_predictor is None:
                return JsonResponse({
                    'success': True,
                    'answer': 'Sorry, the chatbot is currently unavailable. The model needs to be trained first. Please contact the administrator.',
                    'confidence': 0.0
                })
            
            # Get response from chatbot
            result = bot_predictor.get_answer(question)
            
            # Add disclaimer if not emergency
            if not result.get('is_emergency', False):
                result['answer'] += bot_predictor.get_disclaimer()
            
            # Get or create session ID
            session_id = request.session.get('chat_session_id', str(uuid.uuid4()))
            request.session['chat_session_id'] = session_id
            
            # Save to chat history
            ChatHistory.objects.create(
                user=request.user,
                question=question,
                answer=result['answer'],
                confidence_score=result['confidence'],
                session_id=session_id
            )
            
            return JsonResponse({
                'success': True,
                'answer': result['answer'],
                'confidence': result['confidence'],
                'category': result.get('category', 'general'),
                'is_emergency': result.get('is_emergency', False)
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON data'
            })
        except Exception as e:
            print(f"Error in send_message: {e}")
            return JsonResponse({
                'success': False,
                'error': 'An error occurred. Please try again.'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Invalid request method'
    })


@login_required
def clear_chat(request):
    """Clear chat history"""
    if request.method == 'POST':
        session_id = request.session.get('chat_session_id')
        if session_id:
            ChatHistory.objects.filter(
                user=request.user,
                session_id=session_id
            ).delete()
            
            # Create new session
            request.session['chat_session_id'] = str(uuid.uuid4())
        
        messages.success(request, 'Chat history cleared!')
        return redirect('chat')
    
    return redirect('chat')


@login_required
def find_doctors(request):
    """Find doctors near user location"""
    # Get all active doctors
    doctors = Doctor.objects.filter(is_active=True)[:20]
    
    context = {
        'doctors': doctors,
        'google_api_key': settings.GOOGLE_PLACES_API_KEY
    }
    
    return render(request, 'bot/find_doctors.html', context)


@login_required
def find_hospitals(request):
    """Find hospitals near user location"""
    # Get all active hospitals
    hospitals = Hospital.objects.filter(is_active=True)[:20]
    
    context = {
        'hospitals': hospitals,
        'google_api_key': settings.GOOGLE_PLACES_API_KEY
    }
    
    return render(request, 'bot/find_hospitals.html', context)


@login_required
def chat_history_view(request):
    """View all chat history"""
    history = ChatHistory.objects.filter(user=request.user).order_by('-timestamp')[:100]
    
    context = {
        'history': history
    }
    return render(request, 'bot/chat_history.html', context)