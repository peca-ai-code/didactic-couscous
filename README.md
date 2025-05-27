# 🏥 Gynecology Chatbot

A secure, privacy-focused AI-powered chatbot providing gynecological health information and appointment booking services. The system combines multiple AI models to deliver the most relevant and helpful responses to users' health-related questions.

## ⚠️ **Important Medical Disclaimer**

**This chatbot is for informational and educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition. Never disregard professional medical advice or delay in seeking it because of something you have read in this chat.**

**In case of a medical emergency, please contact your local emergency services immediately.**

---

## 🌟 Features

### Core Functionality
- **Multi-Model AI Integration**: Combines responses from OpenAI GPT, Google Gemini, and Grok for comprehensive answers
- **Intelligent Response Selection**: Automatically selects the best response based on quality and relevance
- **Conversation Management**: Persistent chat history with secure storage
- **Severity Assessment**: AI-powered assessment of health concerns with appropriate urgency indicators
- **Smart Appointment Booking**: Integrated appointment scheduling with gynecologists

### Security & Privacy
- **User Authentication**: JWT-based secure authentication system
- **Data Encryption**: Secure handling of sensitive health conversations
- **Privacy-First Design**: Minimal data collection with user consent
- **Session Management**: Secure session handling with automatic cleanup

### User Experience
- **Responsive Design**: Works seamlessly across desktop and mobile devices
- **Real-time Chat**: Instant responses with typing indicators
- **Doctor Discovery**: Browse and filter gynecologists by specialty, rating, and availability
- **Appointment Management**: Complete booking system with calendar integration

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Chainlit      │    │   Django REST   │    │   AI Services   │
│   Frontend      │◄──►│     Backend     │◄──►│  (OpenAI, etc.) │
│  (Port 8001)    │    │   (Port 9000)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   SQLite DB     │
                       │  (Development)  │
                       └─────────────────┘
```

### Technology Stack

**Backend:**
- **Django 5.0.6** - Web framework
- **Django REST Framework** - API development
- **SQLite** - Database (development) / **PostgreSQL** (production recommended)
- **JWT Authentication** - Secure user authentication
- **CORS** - Cross-origin resource sharing

**Frontend:**
- **Chainlit** - Conversational AI interface
- **React** - Appointment booking system
- **Tailwind CSS** - Styling

**AI Integration:**
- **OpenAI GPT-4** - Primary language model
- **Google Gemini** - Secondary model and evaluation
- **Grok** - Fallback model

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Node.js 16+** (optional, for frontend development)
- **Git**

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/peca-ai-code/didactic-couscous.git
cd gynecology-chatbot
```

2. **Set up the backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

4. **Set up the database**
```bash
python manage.py migrate
python manage.py createsuperuser
python create_guest_user.py  # Creates guest user and generates JWT token
```

5. **Set up the frontend**
```bash
cd ../chainlit_app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add the JWT token from step 4 to DJANGO_API_TOKEN
```

6. **Start both servers**
```bash
cd ..
chmod +x run_servers.sh
./run_servers.sh
```

The application will be available at:
- **Chat Interface**: http://localhost:8001
- **Django Admin**: http://localhost:9000/admin
- **Appointment Booking**: http://localhost:9000/appointments

---

## ⚙️ Configuration

### Environment Variables

#### Backend (`.env`)
```env
# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True

# AI Service API Keys
OPENAI_API_KEY=your-openai-api-key
GEMINI_API_KEY=your-gemini-api-key
GROK_API_KEY=your-grok-api-key

# Model Configuration (Optional)
OPENAI_MODEL=gpt-4o
GEMINI_MODEL=gemini-1.5-flash
GROK_MODEL=grok-2
```

#### Frontend (`.env`)
```env
# Django Backend Configuration
DJANGO_API_URL=http://localhost:9000/api
DJANGO_API_TOKEN=your-jwt-token-from-create-guest-user-script

# AI Configuration
GEMINI_API_KEY=your-gemini-api-key
```

### Obtaining API Keys

1. **OpenAI API Key**
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create an account and generate an API key
   - Add billing information for usage

2. **Google Gemini API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - No billing required for basic usage

3. **Grok API Key** (Optional)
   - Currently simulated in the codebase
   - Replace with actual implementation when available

---

## 📖 Usage

### For End Users

1. **Access the chat interface** at http://localhost:8001
2. **Start a conversation** by typing your gynecological health question
3. **Review the AI response** and any severity indicators
4. **Book an appointment** if recommended by the system
5. **Browse available doctors** and schedule consultations

### For Administrators

1. **Access Django Admin** at http://localhost:9000/admin
2. **Manage users** and their conversations
3. **Monitor chat interactions** and system health
4. **Configure system settings** and AI model preferences

---

## 🔌 API Documentation

### Authentication
All API endpoints require JWT authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### Core Endpoints

#### Conversations
```http
GET /api/chatbot/conversations/          # List conversations
POST /api/chatbot/conversations/         # Create conversation
GET /api/chatbot/conversations/{id}/     # Get conversation details
DELETE /api/chatbot/conversations/{id}/clear/  # Clear conversation messages
POST /api/chatbot/conversations/{id}/send_message/  # Send message
```

#### Users
```http
GET /api/users/me/                       # Get current user profile
PUT /api/users/update_settings/          # Update user settings
POST /api/users/register/                # Register new user
```

#### Health & Utilities
```http
GET /api/health/                         # Health check
GET /api/placeholder/{width}/{height}    # Generate placeholder images
```

### Request/Response Examples

**Send Message:**
```json
POST /api/chatbot/conversations/1/send_message/
{
  "message": "I'm experiencing irregular periods. Should I be concerned?"
}

Response:
{
  "message_id": 123,
  "content": "Irregular periods can have various causes...",
  "model_name": "gemini",
  "explanation": "Selected best response based on medical accuracy"
}
```

---

## 🧪 Testing

### Running Tests
```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests (if implemented)
cd chainlit_app
python -m pytest tests/
```

### Manual Testing Checklist
- [ ] User registration and authentication
- [ ] Chat conversation flow
- [ ] AI response generation from multiple models
- [ ] Appointment booking system
- [ ] Admin panel functionality
- [ ] API endpoint responses

---

## 🚀 Deployment

### Production Considerations

1. **Database**: Switch from SQLite to PostgreSQL
2. **Environment**: Set `DEBUG=False` and configure proper `ALLOWED_HOSTS`
3. **Security**: Implement HTTPS, security headers, and rate limiting
4. **Monitoring**: Add application monitoring and error tracking
5. **Backup**: Implement database backup strategy

### Docker Deployment (Recommended)

```dockerfile
# Example Dockerfile structure
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "gynecology_chatbot_project.wsgi:application"]
```

### Environment Variables for Production
```env
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgres://user:pass@host:port/dbname
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
```

---

## 🤝 Contributing

We welcome contributions to improve the gynecology chatbot! Please follow these guidelines:

### Development Workflow

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** with appropriate tests
4. **Follow code style**: Use `black` for Python formatting
5. **Test thoroughly**: Ensure all tests pass
6. **Commit changes**: `git commit -m 'Add amazing feature'`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Code Standards

- **Python**: Follow PEP 8, use type hints where beneficial
- **Documentation**: Update README and docstrings for new features
- **Testing**: Maintain >80% code coverage
- **Security**: Never commit secrets or sensitive data

### Areas for Contribution

- **AI Model Integration**: Add support for new language models
- **Medical Content**: Improve system prompts and response quality
- **Security**: Enhance authentication and data protection
- **Testing**: Expand test coverage and add integration tests
- **Documentation**: Improve user guides and API documentation
- **Accessibility**: Enhance UI/UX for diverse users

---

## 🔒 Security

### Security Features

- **JWT Authentication** with token rotation
- **Input validation** and sanitization
- **Rate limiting** on API endpoints
- **CORS protection** with whitelist origins
- **SQL injection protection** via Django ORM
- **XSS protection** with content security policies

---

## 📋 Roadmap

### Version 1.0 (Current)
- [x] Basic chat interface with AI integration
- [x] Multi-model response evaluation
- [x] User authentication system
- [x] Appointment booking integration

### Version 1.1 (Planned)
- [ ] Enhanced medical content filtering
- [ ] User feedback and rating system
- [ ] Mobile app development
- [ ] Integration with telehealth platforms

### Version 2.0 (Future)
- [ ] Multi-language support
- [ ] Voice interaction capabilities
- [ ] Advanced health tracking features
- [ ] Integration with wearable devices

---

## 🙏 Acknowledgments

- **Medical Advisory Board**: [List medical professionals who reviewed content]
- **AI Models**: OpenAI, Google, and X.AI for providing AI capabilities
- **Open Source Community**: For the amazing tools and libraries
- **Beta Testers**: Users who provided valuable feedback during development

---

## ⚖️ Legal Disclaimers

### Medical Disclaimer
This software is provided for informational purposes only. It is not intended to be a substitute for professional medical advice, diagnosis, or treatment. The developers and contributors are not medical professionals and do not provide medical advice.

### Liability Limitation
The software is provided "as is" without warranty of any kind. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability arising from the use of this software.

### Privacy Statement
We are committed to protecting user privacy. Please review our Privacy Policy for detailed information about data collection, usage, and protection practices.

---

**Made with ❤️ for women's health**