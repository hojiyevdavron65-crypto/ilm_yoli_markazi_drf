from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth import get_user_model

User = get_user_model()


class IsAdminOrReadOnly(BasePermission):
    """
    Kurs va guruhlarni o'qish (GET) barchaga ochiq (ro'yxatdan o'tganlarga).
    Yaratish, tahrirlash va o'chirish faqat Admin foydalanuvchilar uchun.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated

        return (
                request.user
                and request.user.is_authenticated
                and (request.user.role == User.Role.ADMIN or request.user.is_superuser)
        )