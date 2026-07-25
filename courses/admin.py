from django.contrib import admin
from .models import Course, Group


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'course', 'teacher', 'created_at')
    search_fields = ('name', 'course__name', 'teacher__username')
    list_filter = ('course', 'teacher')