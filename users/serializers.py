from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "phone", "role"]
        read_only_fields = ["id", "role"]   # role'ni o'zi o'zgartira olmaydi


class UserListSerializer(serializers.ModelSerializer):
    """Admin uchun — hammasi ko'rinadi"""
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "phone", "role", "is_active"]