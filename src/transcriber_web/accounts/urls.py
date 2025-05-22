from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path(
        "recover_password/",
        views.RecoverPasswordView.as_view(),
        name="recover_password",
    ),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "change_password/", views.ChangePasswordView.as_view(), name="change_password"
    ),
    path("profile/", views.ProfileView.as_view(), name="profile"),
]
