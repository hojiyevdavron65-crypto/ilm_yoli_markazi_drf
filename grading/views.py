from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Grade
from .serializers import GradeSerializer
from .permissions import IsTeacherOrAdminForGrading

User = get_user_model()


class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdminForGrading]

    def get_queryset(self):
        user = self.request.user

        # 1. Admin barcha baholarni ko'radi
        if user.role == User.Role.ADMIN or user.is_superuser:
            return Grade.objects.all()

        # 2. Ustoz o'zi dars beradigan guruhdagi baholarni ko'radi
        elif user.role == User.Role.TEACHER:
            return Grade.objects.filter(group__teacher=user)

        # 3. O'QUVCHI FAQAT VA FAQAT O'Z BAHOLARINI KO'RADI (Maxfiy va muhim)
        return Grade.objects.filter(student=user)