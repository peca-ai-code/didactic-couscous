import os
import time
import openai
import google.generativeai as genai
from django.conf import settings

# Configure API clients
openai.api_key = settings.OPENAI_API_KEY
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

# Keep the async functions but add synchronous versions

async def get_openai_response(user_message, chat_history=None):
    """Async version - kept for completeness but not used"""
    return get_openai_response_sync(user_message, chat_history)

def get_openai_response_sync(user_message, chat_history=None):
    """Synchronous version for OpenAI response"""
    if not settings.OPENAI_API_KEY:
        print("OpenAI API key is missing!")
        return "Error: OpenAI API key not configured."
    
    try:
        # Create messages array with system prompt
        messages = [{"role": "system", "content": settings.GYNECOLOGY_SYSTEM_PROMPT}]
        
        # Add chat history if provided
        if chat_history:
            for msg in chat_history:
                role = "user" if msg.message_type == "user" else "assistant"
                messages.append({"role": role, "content": msg.content})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call OpenAI API
        client = openai.Client(api_key=settings.OPENAI_API_KEY)  # Use sync client
        response = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        print(f"OpenAI response generated successfully")
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"OpenAI error: {str(e)}")
        return f"Error generating response from ChatGPT: {str(e)}"

async def get_gemini_response(user_message, chat_history=None):
    """Async version - kept for completeness but not used"""
    return get_gemini_response_sync(user_message, chat_history)

def get_gemini_response_sync(user_message, chat_history=None):
    """Synchronous version for Gemini response"""
    if not settings.GEMINI_API_KEY:
        print("Gemini API key is missing!")
        return "Error: Gemini API key not configured."
    
    try:
        # Format history for Gemini
        formatted_history = []
        
        # Add system instruction
        formatted_history.append({
            "role": "user",
            "parts": [{"text": settings.GYNECOLOGY_SYSTEM_PROMPT}]
        })
        
        # Add chat history if provided
        if chat_history:
            for msg in chat_history:
                role = "user" if msg.message_type == "user" else "model"
                formatted_history.append({
                    "role": role,
                    "parts": [{"text": msg.content}]
                })
        
        # Add current user message
        formatted_history.append({
            "role": "user",
            "parts": [{"text": user_message}]
        })
        
        # Generate response
        generation_config = {
            "temperature": 0.7,
            "max_output_tokens": 500,
        }
        
        model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            generation_config=generation_config
        )
        
        response = model.generate_content(formatted_history)
        print(f"Gemini response generated successfully")
        
        if hasattr(response, 'text'):
            return response.text
        else:
            return "Error: Gemini returned an unexpected response format."
            
    except Exception as e:
        print(f"Gemini error: {str(e)}")
        return f"Error generating response from Gemini: {str(e)}"

async def get_grok_response(user_message, chat_history=None):
    """Async version - kept for completeness but not used"""
    return get_grok_response_sync(user_message, chat_history)

def get_grok_response_sync(user_message, chat_history=None):
    """Synchronous version for simulated Grok response"""
    # Simulate API delay
    time.sleep(1) 
    
    return (
        f"As your gynecology assistant, I understand you're asking about '{user_message[:30]}...'. "
        f"While I don't have complete information, I can provide general guidance on this topic. "
        f"Remember to consult with a healthcare provider for a proper evaluation of your specific situation."
    )