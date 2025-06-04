#backend/gynecology_chatbot_project/settings_production.py
import os
import environ
from google.oauth2 import service_account
from .settings import *

# Initialize environ
env = environ.Env(
    DEBUG=(bool, False)
)

# Security Settings
DEBUG = False
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

# Allowed hosts for Cloud Run
ALLOWED_HOSTS = [
    '.run.app',
    '.a.run.app',
    'localhost',
    '127.0.0.1',
]

# Add your custom domain here when you set it up
if os.environ.get('CUSTOM_DOMAIN'):
    ALLOWED_HOSTS.append(os.environ.get('CUSTOM_DOMAIN'))

# Database Configuration for Cloud SQL
if os.environ.get('USE_CLOUD_SQL') == 'true':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': f'/cloudsql/{os.environ.get("CLOUD_SQL_CONNECTION_NAME")}',
            'PORT': '5432',
        }
    }
else:
    # Use SQLite for development/testing
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/db.sqlite3',  # Use /tmp for Cloud Run
        }
    }

# Static Files with WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS Settings for production
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    f"https://{os.environ.get('FRONTEND_DOMAIN', 'localhost:8001')}",
]

# Add your Chainlit Cloud Run URL here after deployment
if os.environ.get('CHAINLIT_URL'):
    CORS_ALLOWED_ORIGINS.append(os.environ.get('CHAINLIT_URL'))

# Frontend URL for production redirects
FRONTEND_URL = os.getenv('FRONTEND_URL', os.getenv('CHAINLIT_URL', 'http://localhost:8001'))

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
