import asyncio
from typing import Dict, List, Any, Tuple
import google.generativeai as genai
from django.conf import settings
import threading
import time
from apps.chatbot.api import get_openai_response_sync, get_gemini_response_sync, get_grok_response_sync

# Configure Gemini for evaluation
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_all_responses_sync(user_message: str, chat_history: List[Any]) -> Dict[str, str]:
    """Generate responses from all AI models using threads."""
    # Initialize response dictionary
    response_dict = {}
    
    # Define functions to run in threads
    def get_openai():
        try:
            response = get_openai_response_sync(user_message, chat_history)
            if response and not response.startswith("Error"):
                response_dict["openai"] = response
        except Exception as e:
            print(f"OpenAI thread error: {str(e)}")
    
    def get_gemini():
        try:
            response = get_gemini_response_sync(user_message, chat_history)
            if response and not response.startswith("Error"):
                response_dict["gemini"] = response
        except Exception as e:
            print(f"Gemini thread error: {str(e)}")
    
    def get_grok():
        try:
            response = get_grok_response_sync(user_message, chat_history)
            if response:
                response_dict["grok"] = response
        except Exception as e:
            print(f"Grok thread error: {str(e)}")
    
    # Create and start threads
    threads = [
        threading.Thread(target=get_openai),
        threading.Thread(target=get_gemini),
        threading.Thread(target=get_grok)
    ]
    
    for thread in threads:
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    return response_dict

def evaluate_responses_sync(responses: Dict[str, str], user_message: str) -> Tuple[str, str, str]:
    """
    Use Gemini to evaluate and select the best response from multiple LLMs.
    Prioritize Gemini when available.
    """
    # If only one response is available, return it without evaluation
    if len(responses) == 1:
        model_name = list(responses.keys())[0]
        return model_name, responses[model_name], "Only one model response was available."
    
    # If no responses available, return error
    if not responses:
        return "system", "I'm sorry, all AI models are currently unavailable. Please try again later.", ""
    
    try:
        # If Gemini API key is not available or evaluation fails, return Gemini first (if available), then others
        if "gemini" in responses:
            return "gemini", responses["gemini"], "Gemini response selected as default."
        elif "openai" in responses:
            return "openai", responses["openai"], "OpenAI response selected."
        else:
            model_name = list(responses.keys())[0]
            return model_name, responses[model_name], "Default response selected."
        
    except Exception as e:
        # Prioritize Gemini in the fallback case too
        if "gemini" in responses:
            return "gemini", responses["gemini"], f"Fallback to Gemini due to error: {str(e)}"
        elif "openai" in responses:
            return "openai", responses["openai"], f"Fallback to OpenAI due to error: {str(e)}"
        elif "grok" in responses:
            return "grok", responses["grok"], f"Fallback to Grok due to error: {str(e)}"
        else:
            # This should never happen, but just in case
            default_model = list(responses.keys())[0]
            return default_model, responses[default_model], f"Evaluation error: {str(e)}"

def generate_ai_responses(user_message: str, chat_history: List[Any]) -> Dict[str, Any]:
    """
    Generate responses from multiple models and select the best one.
    This is a fully synchronous implementation with Gemini as the preferred fallback.
    """
    try:
        # Get responses from all models
        all_responses = generate_all_responses_sync(user_message, chat_history)
        
        # Evaluate and select the best response
        best_model, best_response, explanation = evaluate_responses_sync(all_responses, user_message)
        
        return {
            "all_responses": all_responses,
            "best_model": best_model,
            "best_response": best_response,
            "explanation": explanation
        }
    except Exception as e:
        print(f"Error in generate_ai_responses: {str(e)}")
        
        # Try Gemini first as fallback
        try:
            gemini_response = get_gemini_response_sync(user_message, chat_history)
            if gemini_response and not gemini_response.startswith("Error"):
                return {
                    "all_responses": {"gemini": gemini_response},
                    "best_model": "gemini",
                    "best_response": gemini_response,
                    "explanation": f"Fallback to Gemini due to error: {str(e)}"
                }
        except Exception as gemini_error:
            print(f"Gemini fallback error: {str(gemini_error)}")
        
        # If Gemini fails, use Grok as the final fallback
        grok_response = get_grok_response_sync(user_message, chat_history)
        return {
            "all_responses": {"grok": grok_response},
            "best_model": "grok",
            "best_response": grok_response,
            "explanation": f"Fallback to Grok after both evaluation and Gemini fallback failed."
        }