from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Custom user model for the gynecology chatbot."""
    email = models.EmailField(_('email address'), unique=True)
    
    # Additional fields
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Medical-related fields
    has_accepted_terms = models.BooleanField(default=False)
    
    # Settings
    preferred_model = models.CharField(
        max_length=20, 
        choices=[
            ('openai', 'ChatGPT'),
            ('gemini', 'Gemini'),
            ('grok', 'Grok'),
        ],
        default='openai'
    )
    show_all_models = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
