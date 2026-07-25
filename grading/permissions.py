from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User = get_user_model()


class IsTeacherOrAdminForGrading(BasePermission):
    """
    Baho qo'yish, tahrirlash va o'chirish faqat Ustoz hamda Admin uchun.
    O'quvchi faqat ko'rish (GET) huquqiga ega.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.role in [User.Role.TEACHER, User.Role.ADMIN] or request.user.is_superuser

        return True