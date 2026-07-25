from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="Kurs nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name="Guruh nomi")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="groups")
    teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': User.Role.TEACHER},
        related_name="teaching_groups"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.course.name})"