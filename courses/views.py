from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import Course, Group
from .serializers import CourseSerializer, GroupSerializer
from .permissions import IsAdminOrReadOnly

User = get_user_model()


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]


class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        # Mantiq: Ustoz bo'lsa, faqat o'zi dars berayotgan guruhlarni ko'radi
        if user.role == User.Role.TEACHER:
            return Group.objects.filter(teacher=user)
        # Admin va O'quvchilar barcha guruhlarni ko'radi
        return Group.objects.all()