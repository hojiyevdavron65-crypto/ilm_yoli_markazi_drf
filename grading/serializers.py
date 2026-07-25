from rest_framework import serializers
from .models import Grade


class GradeSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.get_full_name')
    group_name = serializers.ReadOnlyField(source='group.name')

    class Meta:
        model = Grade
        fields = ['id', 'group', 'group_name', 'student', 'student_name', 'grade', 'comment', 'date', 'created_at']