from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Attendance
from .serializers import AttendanceSerializer
from .permissions import IsTeacherOrAdminForAttendance

User = get_user_model()


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsTeacherOrAdminForAttendance]

    def get_queryset(self):
        user = self.request.user

        # 1. Admin barcha davomatlarni ko'radi
        if user.role == User.Role.ADMIN or user.is_superuser:
            return Attendance.objects.all()

        # 2. Ustoz faqat o'zi dars beradigan guruh davomatini ko'radi
        elif user.role == User.Role.TEACHER:
            return Attendance.objects.filter(group__teacher=user)

        # 3. O'quvchi FAQAT O'ZINING davomatini ko'radi (Talab bajarildi)
        return Attendance.objects.filter(student=user)