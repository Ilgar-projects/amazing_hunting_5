from urllib.parse import urlencode

from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from vacancies.models import Vacancy
from vacancies.web_forms import VacancyWebForm


class SearchView(View):
    template_name = "vacancies/search.html"

    def get(self, request):
        vacancies = (
            Vacancy.objects.select_related("user")
            .prefetch_related("skills")
            .all()
            .order_by("-id")
        )
        q = (request.GET.get("q") or "").strip()
        if q:
            vacancies = vacancies.filter(title__icontains=q) | vacancies.filter(text__icontains=q)
        return render(request, self.template_name, {"vacancies": vacancies, "q": q, "active_nav": "search"})


def _redirect_to_auth(request, tab: str):
    base_url = reverse("auth")
    query = urlencode({"tab": tab, "next": request.get_full_path()})
    return redirect(f"{base_url}?{query}")


class VacancyCreateWebView(View):
    template_name = "vacancies/create.html"

    def get(self, request):
        if not request.user.is_authenticated:
            # По требованиям: на «Создать» показываем регистрацию
            return _redirect_to_auth(request, tab="signup")
        form = VacancyWebForm()
        return render(request, self.template_name, {"form": form, "active_nav": "create"})

    def post(self, request):
        if not request.user.is_authenticated:
            return _redirect_to_auth(request, tab="signup")
        form = VacancyWebForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect("home")
        return render(request, self.template_name, {"form": form, "active_nav": "create"})


class ProfileView(View):
    template_name = "vacancies/profile.html"

    def get(self, request):
        if not request.user.is_authenticated:
            # Профиль без входа не доступен — ведём на вкладку «Вход»
            return _redirect_to_auth(request, tab="login")
        my = Vacancy.objects.filter(user=request.user).prefetch_related("skills").order_by("-id")
        return render(request, self.template_name, {"my_vacancies": my, "active_nav": "profile"})
