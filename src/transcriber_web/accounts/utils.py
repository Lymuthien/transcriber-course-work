from functools import wraps
from django.shortcuts import redirect
from transcriber_web.transcriber_web.services import user_repository


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")

        user = user_repository.get_by_id(request.session["user_id"])
        if not user or user.is_blocked:
            return redirect("login")
        request.user = user

        return view_func(request, *args, **kwargs)

    return wrapper
