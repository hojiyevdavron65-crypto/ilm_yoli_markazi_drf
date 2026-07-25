from django.contrib import admin
from .models import EnrollmentRequest, GroupStudent


@admin.register(EnrollmentRequest)
class EnrollmentRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'group', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'group')
    search_fields = ('student__username', 'group__name')
    actions = ['approve_requests', 'reject_requests']

    @admin.action(description="Tanlangan arizalarni tasdiqlash va guruhga qo'shish")
    def approve_requests(self, request, queryset):
        for enrollment in queryset:
            enrollment.status = EnrollmentRequest.Status.APPROVED
            enrollment.save()
            # Otomatik guruhga a'zo qilish
            GroupStudent.objects.get_or_create(group=enrollment.group, student=enrollment.student)
        self.message_user(request, "Tanlangan arizalar tasdiqlandi!")

    @admin.action(description="Tanlangan arizalarni rad etish")
    def reject_requests(self, request, queryset):
        queryset.update(status=EnrollmentRequest.Status.REJECTED)
        self.message_user(request, "Tanlangan arizalar rad etildi.")


@admin.register(GroupStudent)
class GroupStudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'student', 'joined_at')
    list_filter = ('group',)
    search_fields = ('student__username', 'group__name')