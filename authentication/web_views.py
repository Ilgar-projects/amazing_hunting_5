from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View

from .forms import SignUpForm


class AuthLandingView(View):
    """Страница авторизации: Регистрация (по умолчанию) + вкладка Вход.

    Поддерживает параметр ?next=... чтобы после входа/регистрации
    вернуть пользователя туда, куда он хотел попасть (например, /create/).

    Важно: формы имеют разные prefix, чтобы в HTML не было дубликатов id/name.
    """

    template_name = "authentication/auth_landing.html"

    def _safe_next(self, request, next_url: str) -> str:
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return next_url
        return reverse("home")  # главная = поиск

    def _blank_forms(self, request):
        return SignUpForm(prefix="signup"), AuthenticationForm(request, prefix="login")

    def get(self, request):
        active_tab = request.GET.get("tab", "signup")
        next_url = request.GET.get("next", "")

        signup_form, login_form = self._blank_forms(request)

        context = {
            "signup_form": signup_form,
            "login_form": login_form,
            "active_tab": active_tab,
            "next": next_url,
            "active_nav": "login",
        }
        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get("action", "signup")
        next_url = request.POST.get("next", "") or request.GET.get("next", "")

        signup_form, login_form = self._blank_forms(request)
        active_tab = "signup"

        if action == "login":
            active_tab = "login"
            login_form = AuthenticationForm(request, data=request.POST, prefix="login")
            if login_form.is_valid():
                auth_login(request, login_form.get_user())
                return redirect(self._safe_next(request, next_url))
        else:
            active_tab = "signup"
            signup_form = SignUpForm(request.POST, prefix="signup")
            if signup_form.is_valid():
                user = signup_form.save()
                auth_login(request, user)
                return redirect(self._safe_next(request, next_url))

        context = {
            "signup_form": signup_form,
            "login_form": login_form,
            "active_tab": active_tab,
            "next": next_url,
            "active_nav": "login",
        }
        return render(request, self.template_name, context)
