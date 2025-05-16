from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UsersView.as_view(), name="admin_users"),
    path("create_admin/", views.CreateAdminView.as_view(), name="create_admin"),
]
