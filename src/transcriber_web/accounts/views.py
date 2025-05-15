from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from transcriber_web.services import ServiceContainer
from transcriber_service.domain.exceptions import AuthException


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = ServiceContainer().auth_service.login(email, password)
            request.session["user_id"] = user.id
            return redirect("records_list")
        except AuthException as e:
            return render(request, "accounts/login.html", {"error": str(e)})

    return render(request, "accounts/login.html")


class LoginView(View):
    template_name = "accounts/login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = ServiceContainer().auth_service.login(email, password)
            request.session["user_id"] = user.id
            return redirect("records_list")
        except AuthException as e:
            return render(request, self.template_name, {"error": str(e)})


class RegisterView(View):
    template_name = "accounts/register.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = ServiceContainer().auth_service.register_user(email, password)
            request.session["user_id"] = user.id

            return redirect(reverse_lazy("records_list"))
        except Exception as e:
            return render(request, self.template_name, {"error": str(e)})


# class ChangePasswordView(LoginRequiredMixin, View):
#     template_name = "accounts/change_password.html"
#
#     def get(self, request):
#         return render(request, self.template_name)
#
#     def post(self, request):
#         email = request.user.email
#         current_password = request.POST.get("current_password")
#         new_password = request.POST.get("new_password")
#         try:
#             auth_service.change_password(email, current_password, new_password)
#             return redirect(reverse_lazy("records_list"))
#         except AuthException as e:
#             return render(request, self.template_name, {"error": str(e)})


class RecoverPasswordView(View):
    template_name = "accounts/recover_password.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        try:
            ServiceContainer().auth_service.recover_password(email)
            return render(
                request,
                self.template_name,
                {"message": "Временный пароль отправлен на ваш email"},
            )
        except AuthException as e:
            return render(request, self.template_name, {"error": str(e)})
