from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnrollmentRequestViewSet, GroupStudentViewSet

router = DefaultRouter()
router.register(r'enrollments', EnrollmentRequestViewSet, basename='enrollment')
router.register(r'group-students', GroupStudentViewSet, basename='group-student')

urlpatterns = [
    path('', include(router.urls)),
]