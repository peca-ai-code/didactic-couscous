from django.shortcuts import render
from django.conf import settings
import os


def landing_page(request):
    """Render the landing page with dynamic URLs."""
    
    # Get URLs from environment or use defaults
    if hasattr(settings, 'FRONTEND_URL') and settings.FRONTEND_URL:
        chatbot_url = settings.FRONTEND_URL
    else:
        chatbot_url = os.getenv('FRONTEND_URL', 'http://localhost:8001')
    
    # For appointments, use the current backend URL
    appointment_url = request.build_absolute_uri('/appointments/')
    
    context = {
        'chatbot_url': chatbot_url,
        'appointment_url': appointment_url,
    }
    
    return render(request, 'landing/index.html', context)
