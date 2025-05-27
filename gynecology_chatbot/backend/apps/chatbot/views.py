from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer, ConversationListSerializer,
    MessageSerializer, ChatInputSerializer
)
from utils.llm_utils import generate_ai_responses

class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for chat conversations."""
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return conversations for the current user."""
        return Conversation.objects.filter(user=self.request.user).order_by('-updated_at')
    
    def get_serializer_class(self):
        """Use different serializers for list and detail views."""
        if self.action == 'list':
            return ConversationListSerializer
        return self.serializer_class
    
    def perform_create(self, serializer):
        """Associate the conversation with the current user."""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        """Send a message in a conversation and get the best AI response."""
        conversation = self.get_object()
        serializer = ChatInputSerializer(data=request.data)
        
        if serializer.is_valid():
            user_message = serializer.validated_data['message']
            
            # Save user message
            message = Message.objects.create(
                conversation=conversation,
                content=user_message,
                message_type='user'
            )
            
            # Get conversation history
            history = Message.objects.filter(conversation=conversation).order_by('created_at')
            
            # Generate AI responses and evaluate the best one
            try:
                response_data = generate_ai_responses(user_message, history)
                
                # Extract the best response and metadata
                best_model = response_data["best_model"]
                best_response = response_data["best_response"]
                explanation = response_data["explanation"]
                
                # Save assistant message with the best response
                assistant_message = Message.objects.create(
                    conversation=conversation,
                    content=best_response,
                    message_type='assistant',
                    model_name=best_model,
                    metadata={
                        "explanation": explanation,
                        "evaluated": True
                    }
                )
                
                # Return response data
                return Response({
                    "message_id": assistant_message.id,
                    "content": best_response,
                    "model_name": best_model,
                    "explanation": explanation
                })
            
            except Exception as e:
                return Response(
                    {'error': f'Error generating AI responses: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['delete'])
    def clear(self, request, pk=None):
        """Clear all messages in a conversation."""
        conversation = self.get_object()
        conversation.messages.all().delete()
        return Response({"message": "Conversation cleared successfully"})

class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for messages (read-only)."""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return messages for a specific conversation."""
        conversation_id = self.kwargs.get('conversation_pk')
        return Message.objects.filter(
            conversation_id=conversation_id,
            conversation__user=self.request.user
        ).order_by('created_at')
