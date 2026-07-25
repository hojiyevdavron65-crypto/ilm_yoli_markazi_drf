from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Group

User = get_user_model()


class Attendance(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='attendances',
        limit_choices_to={'role': User.Role.STUDENT}
    )
    date = models.DateField(verbose_name="Dars sanasi")
    is_present = models.BooleanField(default=True, verbose_name="Darsda bormi?")
    reason = models.CharField(max_length=255, blank=True, verbose_name="Sababi (agar kelmagan bo'lsa)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'student', 'date')

    def __str__(self):
        status = "Kelgan" if self.is_present else "Kelmagan"
        return f"{self.student.username} - {self.date} ({status})"