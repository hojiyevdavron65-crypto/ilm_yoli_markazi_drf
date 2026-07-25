from django.urls import path
from . import views

urlpatterns = [
    path("users/me/", views.my_profile, name="my-profile"),
    path("users/me/update/", views.update_my_profile, name="update-profile"),
    path("users/all/", views.all_users, name="all-users"),
    path("users/role/<str:role>/", views.users_by_role, name="users-by-role"),
]