from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import EnrollmentRequest, GroupStudent
from .serializers import EnrollmentRequestSerializer, GroupStudentSerializer
from .permissions import IsAdminOrStudentOwner

User = get_user_model()


class EnrollmentRequestViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentRequestSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStudentOwner]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.ADMIN or user.is_superuser:
            return EnrollmentRequest.objects.all()
        return EnrollmentRequest.objects.filter(student=user)

    def perform_create(self, serializer):
        # Ariza topshiruvchiga avtomatik ravishda hozirgi login qilgan student biriktiriladi
        serializer.save(student=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def approve(self, request, pk=None):
        """Admin arizani tasdiqlashi uchun alohida endpoint: /api/v1/enrollments/{id}/approve/"""
        if request.user.role != User.Role.ADMIN and not request.user.is_superuser:
            return Response({"detail": "Faqat Admin arizani tasdiqlay oladi."}, status=status.HTTP_403_FORBIDDEN)

        enrollment = self.get_object()
        enrollment.status = EnrollmentRequest.Status.APPROVED
        enrollment.save()

        # O'quvchini guruh a'zolariga qo'shamiz
        GroupStudent.objects.get_or_create(group=enrollment.group, student=enrollment.student)

        return Response({"status": "Ariza tasdiqlandi va o'quvchi guruhga qo'shildi."})

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def reject(self, request, pk=None):
        """Admin arizani rad etishi uchun: /api/v1/enrollments/{id}/reject/"""
        if request.user.role != User.Role.ADMIN and not request.user.is_superuser:
            return Response({"detail": "Faqat Admin arizani rad eta oladi."}, status=status.HTTP_403_FORBIDDEN)

        enrollment = self.get_object()
        enrollment.status = EnrollmentRequest.Status.REJECTED
        enrollment.save()

        return Response({"status": "Ariza rad etildi."})


class GroupStudentViewSet(viewsets.ReadOnlyModelViewSet):
    """Guruh a'zolarini ko'rish uchun endpoint"""
    serializer_class = GroupStudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.ADMIN or user.is_superuser:
            return GroupStudent.objects.all()
        elif user.role == User.Role.TEACHER:
            return GroupStudent.objects.filter(group__teacher=user)
        return GroupStudent.objects.filter(student=user)