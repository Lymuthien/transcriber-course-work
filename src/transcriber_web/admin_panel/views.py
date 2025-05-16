from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from transcriber_web.services import ServiceContainer
from accounts.utils import LoginRequiredMixin

container = ServiceContainer()


class UsersView(LoginRequiredMixin, View):
    template_name = "admin_panel/users.html"

    def get(self, request):
        if not request.user.can_block():
            return render(request, "admin_panel/access_denied.html")
        users = container.user_service.get_all()
        return render(request, self.template_name, {"users": users})

    def post(self, request):
        if not request.user.can_block():
            return render(request, "admin_panel/access_denied.html")

        action = request.POST.get("action")
        target_email = request.POST.get("email")
        try:
            if action == "block":
                container.user_service.block_user(request.user, target_email)
            elif action == "unblock":
                container.user_service.unblock_user(request.user, target_email)
            elif action == "delete":
                container.user_service.delete_user(request.user, target_email)
        except (PermissionError, KeyError) as e:
            users = container.user_service.get_all()
            return render(
                request, self.template_name, {"users": users, "error": str(e)}
            )

        return redirect(reverse_lazy("admin_users"))


class CreateAdminView(LoginRequiredMixin, View):
    template_name = "admin_panel/create_admin.html"

    def get(self, request):
        if not request.user.can_block():
            return render(request, "admin_panel/access_denied.html")
        return render(request, self.template_name)

    def post(self, request):
        if not request.user.can_block():
            return render(request, "admin_panel/access_denied.html")

        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            container.auth_service.create_admin(email, password)
            return redirect(reverse_lazy("admin_users"))
        except Exception as e:
            return render(request, self.template_name, {"error": str(e)})
