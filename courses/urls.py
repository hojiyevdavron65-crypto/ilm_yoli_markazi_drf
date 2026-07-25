from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, GroupViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'groups', GroupViewSet, basename='group')

urlpatterns = [
    path('', include(router.urls)),
]