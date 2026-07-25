from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Group

User = get_user_model()


class EnrollmentRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Kutilmoqda'
        APPROVED = 'approved', 'Qabul qilindi'
        REJECTED = 'rejected', 'Rad etildi'

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollment_requests',
        limit_choices_to={'role': User.Role.STUDENT}
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='enrollment_requests'
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'group')

    def __str__(self):
        return f"{self.student.username} -> {self.group.name} ({self.get_status_display()})"


class GroupStudent(models.Model):
    """Guruhga rasman qabul qilingan o'quvchilar jadvali"""
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrolled_groups')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.group.name}"