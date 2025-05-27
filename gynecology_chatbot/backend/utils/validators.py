from django.core.exceptions import ValidationError
import re

def validate_message_content(content):
    """Validate that message content is not empty or too long."""
    if not content or content.isspace():
        raise ValidationError("Message content cannot be empty.")
    
    if len(content) > 10000:
        raise ValidationError("Message content is too long (max 10000 characters).")

def validate_email(email):
    """Validate email format."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise ValidationError("Invalid email format.")
