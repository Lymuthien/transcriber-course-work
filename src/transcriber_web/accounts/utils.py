from django.shortcuts import redirect
from django.urls import reverse_lazy

from functools import wraps
from transcriber_web.services import ServiceContainer


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")

        user = ServiceContainer().user_repository.get_by_id(request.session["user_id"])
        if not user or user.is_blocked:
            return redirect("login")
        request.user = user

        return view_func(request, *args, **kwargs)

    return wrapper


class LoginRequiredMixin:
    """
    Миксин для проверки аутентификации пользователя.
    Перенаправляет на страницу логина, если пользователь не аутентифицирован или заблокирован.
    """

    def dispatch(self, request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect(reverse_lazy("login"))

        user = ServiceContainer().user_repository.get_by_id(request.session["user_id"])
        if not user or user.is_blocked:
            return redirect(reverse_lazy("login"))
        request.user = user
        return super().dispatch(request, *args, **kwargs)
