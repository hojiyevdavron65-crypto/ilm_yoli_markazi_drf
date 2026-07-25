from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer, UserListSerializer
from .permissions import IsAdmin


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_profile(request):
    """Har qanday login qilgan user o'z profilini ko'radi"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_my_profile(request):
    """User o'z profilini yangilaydi (role'siz)"""
    partial = request.method == "PATCH"
    serializer = UserSerializer(request.user, data=request.data, partial=partial)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAdmin])
def all_users(request):
    """Faqat admin — barcha user'larni ko'radi"""
    users = User.objects.all().order_by("-date_joined")
    serializer = UserListSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAdmin])
def users_by_role(request, role):
    """Faqat admin — role bo'yicha filtrlab ko'radi (masalan: /api/users/teachers/)"""
    if role not in ["admin", "teacher", "student"]:
        return Response({"error": "Noto'g'ri role"}, status=status.HTTP_400_BAD_REQUEST)

    users = User.objects.filter(role=role)
    serializer = UserListSerializer(users, many=True)
    return Response(serializer.data)