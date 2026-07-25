from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User = get_user_model()


class IsTeacherOrAdminForAttendance(BasePermission):
    """
    Davomat yaratish/tahrirlash faqat Ustoz va Admin uchun.
    O'quvchilar faqat ko'rish imkoniyatiga ega.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.role in [User.Role.TEACHER, User.Role.ADMIN] or request.user.is_superuser

        return True