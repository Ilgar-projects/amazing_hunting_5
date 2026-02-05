from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views import View

from .forms import SignUpForm


class AuthLandingView(View):
    """Главная страница: Регистрация (по умолчанию) + вкладка Вход."""

    template_name = "authentication/auth_landing.html"

    def get(self, request):
        active_tab = request.GET.get("tab", "signup")
        context = {
            "signup_form": SignUpForm(),
            "login_form": AuthenticationForm(request),
            "active_tab": active_tab,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        # какая кнопка нажата
        action = request.POST.get("action", "signup")

        signup_form = SignUpForm()
        login_form = AuthenticationForm(request)
        active_tab = "signup"

        if action == "login":
            active_tab = "login"
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                auth_login(request, login_form.get_user())
                return redirect("home")
        else:
            active_tab = "signup"
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                auth_login(request, user)
                return redirect("home")

        context = {
            "signup_form": signup_form,
            "login_form": login_form,
            "active_tab": active_tab,
        }
        return render(request, self.template_name, context)
