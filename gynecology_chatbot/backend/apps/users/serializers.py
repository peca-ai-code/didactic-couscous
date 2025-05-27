from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 
                  'date_of_birth', 'has_accepted_terms', 'preferred_model', 
                  'show_all_models')
        read_only_fields = ('id', 'email')

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 
                  'last_name', 'date_of_birth', 'has_accepted_terms')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            date_of_birth=validated_data.get('date_of_birth', None),
            has_accepted_terms=validated_data.get('has_accepted_terms', False),
        )
        return user

class UserSettingsSerializer(serializers.ModelSerializer):
    """Serializer for user chat settings."""
    
    class Meta:
        model = User
        fields = ('preferred_model', 'show_all_models')
