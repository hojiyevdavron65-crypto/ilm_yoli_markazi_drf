from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from courses.models import Group

User = get_user_model()


class Grade(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='grades')
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='grades',
        limit_choices_to={'role': User.Role.STUDENT}
    )
    grade = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name="Baho (1-100)"
    )
    comment = models.CharField(max_length=255, blank=True, verbose_name="Izoh")
    date = models.DateField(auto_now_add=True, verbose_name="Qo'yilgan sana")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.group.name}: {self.grade}"