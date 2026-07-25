from rest_framework import serializers
from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.get_full_name')
    group_name = serializers.ReadOnlyField(source='group.name')

    class Meta:
        model = Attendance
        fields = ['id', 'group', 'group_name', 'student', 'student_name', 'date', 'is_present', 'reason', 'created_at']