from typing import Any

from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    # write_only will exclude pass. from a response
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model =User
        fields = ['id', 'username', 'email', 'password']
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    