from rest_framework import serializers
from .models import Course, Group


class GroupSerializer(serializers.ModelSerializer):
    course_name = serializers.ReadOnlyField(source='course.name')
    teacher_name = serializers.ReadOnlyField(source='teacher.get_full_name')

    class Meta:
        model = Group
        fields = ['id', 'name', 'course', 'course_name', 'teacher', 'teacher_name', 'created_at']


class CourseSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'groups', 'created_at']