"""
API client for communicating with the Django backend.
"""

import aiohttp
import os
from typing import Dict, Any, Optional, List

class DjangoAPIClient:
    """Client for Django backend API interactions."""
    
    def __init__(self, base_url: str):
        """Initialize the API client with base URL."""
        self.base_url = base_url
        self.token = os.getenv("DJANGO_API_TOKEN", "")
        self.session = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create an aiohttp session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        authenticate: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Make an HTTP request to the API."""
        url = f"{self.base_url}/{endpoint}"
        headers = {}
        
        if authenticate and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        
        if data is not None:
            headers["Content-Type"] = "application/json"
        
        session = await self._get_session()
        
        try:
            async with session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers
            ) as response:
                if response.status in (200, 201):
                    return await response.json()
                else:
                    error_text = await response.text()
                    print(f"API Error: {response.status} - {error_text}")
                return None
        except Exception as e:
            print(f"API request error: {str(e)}")
            return None
    
    async def check_health(self) -> bool:
        """Check if the backend is available."""
        try:
            session = await self._get_session()
            async with session.get(f"{self.base_url}/health/") as response:
                return response.status == 200
        except Exception as e:
            print(f"Health check error: {str(e)}")
            return False
    
    async def authenticate(self, token: str) -> bool:
        """Authenticate with the backend using a token."""
        self.token = token
        
        # Try to get user profile to verify token
        user_data = await self._request("GET", "users/me/")
        return user_data is not None
    
    async def get_user_settings(self) -> Optional[Dict[str, Any]]:
        """Get the current user's settings."""
        user_data = await self._request("GET", "users/me/")
        
        if user_data:
            return {
                "preferred_model": user_data.get("preferred_model", "openai"),
                "show_all_models": user_data.get("show_all_models", True)
            }
        return None
    
    async def create_conversation(self, title: str) -> Optional[Dict[str, Any]]:
        """Create a new conversation."""
        data = {"title": title}
        return await self._request("POST", "chatbot/conversations/", data=data)
    
    async def get_conversations(self) -> List[Dict[str, Any]]:
        """Get the list of conversations for the current user."""
        response = await self._request("GET", "chatbot/conversations/")
        return response or []
    
    async def get_conversation(self, conversation_id: int) -> Optional[Dict[str, Any]]:
        """Get a specific conversation with its messages."""
        return await self._request("GET", f"chatbot/conversations/{conversation_id}/")
    
    async def send_message(
        self,
        conversation_id: int,
        message: str,
    ) -> Optional[Dict[str, Any]]:
        """Send a message to the conversation and get AI response."""
        data = {
            "message": message
        }
        
        return await self._request(
            "POST", 
            f"chatbot/conversations/{conversation_id}/send_message/", 
            data=data
        )
    
    async def clear_conversation(self, conversation_id: int) -> bool:
        """Clear all messages in a conversation."""
        response = await self._request(
            "DELETE", 
            f"chatbot/conversations/{conversation_id}/clear/"
        )
        return response is not None
    
    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close()
