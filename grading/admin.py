from django.contrib import admin
from .models import Grade


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'student', 'grade', 'date', 'created_at')
    list_filter = ('group', 'date', 'grade')
    search_fields = ('student__username', 'group__name')