from rest_framework import serializers
from .models import User, FriendRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'timestamp', 'accepted']
        read_only_fields = ['from_user', 'timestamp', 'accepted']
