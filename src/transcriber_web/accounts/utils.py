import logging

from django.shortcuts import redirect
from django.urls import reverse_lazy

from transcriber_web.services import ServiceContainer

logger = logging.getLogger(__name__)


class LoginRequiredMixin:

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, "dispatch"):
            logger.error("Class doesn't have dispatch method")
            raise AttributeError(
                "LoginRequiredMixin must be used with a class that defines 'dispatch' method"
            )

        if "user_id" not in request.session:
            logger.warning("User id not found in session")
            return redirect(reverse_lazy("login"))

        user = ServiceContainer().user_service.get_by_id(request.session["user_id"])
        if not user or user.is_blocked:
            logger.warning("User is blocked or does not exist")
            return redirect(reverse_lazy("login"))
        request.user = user

        logger.info(f"User logged in as {user.email}")
        return super().dispatch(request, *args, **kwargs)
