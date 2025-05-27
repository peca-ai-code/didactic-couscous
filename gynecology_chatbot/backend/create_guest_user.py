import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gynecology_chatbot_project.settings')
django.setup()

from apps.users.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# Create a guest user
try:
    user = User.objects.get(username='guest')
    print("Guest user already exists")
except User.DoesNotExist:
    user = User.objects.create_user(
        username='guest',
        email='guest@example.com',
        password='guestpassword123'
    )
    user.save()
    print("Created guest user")

# Generate JWT token
refresh = RefreshToken.for_user(user)
print("\nCopy the following JWT token to your .env file:")
print(f"DJANGO_API_TOKEN={refresh.access_token}")
