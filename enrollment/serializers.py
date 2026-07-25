from rest_framework import serializers
from .models import EnrollmentRequest, GroupStudent


class EnrollmentRequestSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.get_full_name')
    group_name = serializers.ReadOnlyField(source='group.name')

    class Meta:
        model = EnrollmentRequest
        fields = ['id', 'student', 'student_name', 'group', 'group_name', 'status', 'created_at']
        read_only_fields = ['student', 'status', 'created_at']


class GroupStudentSerializer(serializers.ModelSerializer):
    student_name = serializers.ReadOnlyField(source='student.get_full_name')
    group_name = serializers.ReadOnlyField(source='group.name')

    class Meta:
        model = GroupStudent
        fields = ['id', 'group', 'group_name', 'student', 'student_name', 'joined_at']