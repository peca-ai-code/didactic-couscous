"""
Chainlit application for gynecology chatbot that communicates with Django backend.
Production-ready version for Cloud Run deployment.
"""

import os
import chainlit as cl
from dotenv import load_dotenv
from services.api_client import DjangoAPIClient
import uuid
import google.generativeai as genai
import webbrowser
import logging

# Configure logging for Cloud Run
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure Gemini for severity assessment
if os.getenv("GEMINI_API_KEY"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize API client with production URL
backend_url = os.getenv("DJANGO_API_URL", "http://localhost:9000/api")
logger.info(f"Connecting to backend at: {backend_url}")

api_client = DjangoAPIClient(base_url=backend_url)

# Set authentication token if available
if os.getenv("DJANGO_API_TOKEN"):
    api_client.token = os.getenv("DJANGO_API_TOKEN")
    logger.info("API token configured")
else:
    logger.warning("No API token found - some features may not work")

@cl.on_chat_start
async def on_chat_start():
    """Initialize the chat session."""
    logger.info("Starting new chat session")
    
    # Generate a unique session identifier
    session_id = str(uuid.uuid4())
    cl.user_session.set("session_id", session_id)
    
    # Check if backend is available
    try:
        backend_status = await api_client.check_health()
        logger.info(f"Backend health check: {backend_status}")
        
        if not backend_status:
            await cl.Message(
                content="⚠️ Warning: Could not connect to the backend server. Please try again later."
            ).send()
            return
    except Exception as e:
        logger.error(f"Backend health check failed: {str(e)}")
        await cl.Message(
            content="⚠️ Error: Backend service is currently unavailable."
        ).send()
        return
    
    # Create a new conversation in the backend
    try:
        conversation = await api_client.create_conversation("New Conversation")
        if conversation:
            conversation_id = conversation.get("id")
            cl.user_session.set("conversation_id", conversation_id)
            logger.info(f"Created conversation: {conversation_id}")
            
            # Welcome message
            await cl.Message(
                content="Welcome to the Gynecology Assistant. I'm here to provide information and support regarding gynecological health concerns. How can I help you today?"
            ).send()
        else:
            logger.error("Failed to create conversation")
            await cl.Message(
                content="⚠️ Error: Could not create conversation. Please check your connection."
            ).send()
    except Exception as e:
        logger.error(f"Error starting chat: {str(e)}")
        await cl.Message(
            content=f"⚠️ Error starting chat: {str(e)}"
        ).send()

def assess_severity(response_text):
    """Assess the severity of a health-related response on a scale of 1-10."""
    try:
        if not os.getenv("GEMINI_API_KEY"):
            logger.warning("Gemini API key is missing for severity assessment")
            return 3  # Default moderate severity if no API key
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        As a medical assessment system, analyze the following gynecological health response and rate its severity on a scale of 1-10.
        1 = Completely routine, no concerns
        5 = Moderate concern that needs attention but isn't urgent
        10 = Very serious, requires immediate medical attention
        
        Provide ONLY a single number (1-10) as your response, no explanation.
        
        Response to assess:
        {response_text}
        """
        
        severity_response = model.generate_content(prompt)
        severity_text = severity_response.text.strip()
        
        # Extract just the number
        severity = 1
        for char in severity_text:
            if char.isdigit():
                severity = int(char)
                break
                
        # Ensure value is between 1-10
        severity = max(1, min(10, severity))
        logger.info(f"Severity assessment: {severity}/10")
        return severity
        
    except Exception as e:
        logger.error(f"Error assessing severity: {str(e)}")
        return 3

@cl.on_message
async def on_message(message: cl.Message):
    """Process user messages and generate responses."""
    logger.info(f"Processing message: {message.content[:50]}...")
    
    # Get session data
    conversation_id = cl.user_session.get("conversation_id")
    
    if not conversation_id:
        # Try to create a new conversation if none exists
        try:
            conversation = await api_client.create_conversation("New Conversation")
            if conversation:
                conversation_id = conversation.get("id")
                cl.user_session.set("conversation_id", conversation_id)
                logger.info(f"Created new conversation: {conversation_id}")
            else:
                await cl.Message(
                    content="Error: Could not create conversation. Please refresh and try again."
                ).send()
                return
        except Exception as e:
            logger.error(f"Error creating conversation: {str(e)}")
            await cl.Message(
                content=f"Error creating conversation: {str(e)}"
            ).send()
            return
    
    # Show thinking message
    # thinking_msg = cl.Message(content="🤔 Thinking...")
    # await thinking_msg.send()
    
    try:
        # Send message to API and get AI response
        response_data = await api_client.send_message(
            conversation_id=conversation_id,
            message=message.content
        )
        
        if not response_data:
            # Handle API error
            await thinking_msg.send(content="Sorry, I encountered an error communicating with the backend. Please try again.")
            return
        
        # Get the best response
        best_response = response_data.get("content", "No response generated.")
        model_name = response_data.get("model_name", "AI")
        
        logger.info(f"Received response from {model_name}")
        
        # Assess severity of the response (1-10 scale)
        severity = assess_severity(best_response)
        
        # Get appointment booking URL from environment or use default
        appointments_url = os.getenv("APPOINTMENTS_URL", "https://gynecology-backend-ffyownlhbq-uc.a.run.app/appointments/")
        
        # Add appointment booking button only if severity is high (>= 4)
        if severity >= 4:
            actions = [
                cl.Action(
                    name="book_appointment", 
                    icon="mouse-pointer-click",
                    payload={"appointments_url": appointments_url},
                    value="book_appointment", 
                    label="🩺 Book a Doctor's Appointment",
                    description="Schedule a consultation with a gynecologist"
                )
            ]
            thinking_msg = cl.Message(content=best_response, actions=actions)
            await thinking_msg.send()
        else:
            thinking_msg = cl.Message(content=best_response)
            await thinking_msg.send()
        
        
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logger.error(f"Error processing message: {str(e)}")
        await thinking_msg.send(content=error_message)

@cl.on_chat_end
async def on_chat_end():
    """Clean up resources when chat ends."""
    logger.info("Chat session ended")
    # Close the API client session
    await api_client.close()

@cl.action_callback("book_appointment")
async def on_book_appointment(action):
    """Handle booking appointment button click."""
    appointments_url = action.payload.get("appointments_url", "https://gynecology-backend-ffyownlhbq-uc.a.run.app/appointments/")
    
    try:
        webbrowser.open(appointments_url)
        # In Cloud Run, we can't open browser, so just provide the link
        await cl.Message(
            content=f"📋 **Book Your Appointment**\n\nPlease visit the following link to book an appointment with a gynecologist:\n\n🔗 [**Click here to book appointment**]({appointments_url})\n\nThis will open our appointment booking system where you can:\n- Browse available doctors\n- Filter by specialty and rating\n- Select convenient time slots\n- Complete your booking"
        ).send()
        
        logger.info(f"Appointment booking link provided: {appointments_url}")
        
    except Exception as e:
        logger.error(f"Error handling appointment booking: {str(e)}")
        await cl.Message(
            content=f"Could not process appointment booking. Please visit: {appointments_url}"
        ).send()
