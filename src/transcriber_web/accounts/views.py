from django.shortcuts import render, redirect
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
