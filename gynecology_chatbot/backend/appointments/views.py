from django.shortcuts import render

def appointment_view(request):
    """Renders the appointments page."""
    return render(request, 'appointments/index.html')
