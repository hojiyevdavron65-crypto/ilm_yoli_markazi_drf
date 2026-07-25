from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'student', 'date', 'is_present', 'created_at')
    list_filter = ('is_present', 'date', 'group')
    search_fields = ('student__username', 'group__name')