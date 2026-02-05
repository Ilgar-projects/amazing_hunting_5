from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from vacancies.models import Vacancy
from vacancies.web_forms import VacancyWebForm


class SearchView(View):
    template_name = "vacancies/search.html"

    def get(self, request):
        # показываем все вакансии (можешь потом фильтровать по status="open")
        vacancies = Vacancy.objects.select_related("user").prefetch_related("skills").all().order_by("-id")
        q = (request.GET.get("q") or "").strip()
        if q:
            vacancies = vacancies.filter(title__icontains=q) | vacancies.filter(text__icontains=q)
        return render(request, self.template_name, {"vacancies": vacancies, "q": q, "active_nav": "search"})


@method_decorator(login_required, name="dispatch")
class CreateVacancyView(View):
    template_name = "vacancies/create.html"

    def get(self, request):
        form = VacancyWebForm()
        return render(request, self.template_name, {"form": form, "active_nav": "create"})

    def post(self, request):
        form = VacancyWebForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect("search")
        return render(request, self.template_name, {"form": form, "active_nav": "create"})


@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    template_name = "vacancies/profile.html"

    def get(self, request):
        my = Vacancy.objects.filter(user=request.user).prefetch_related("skills").order_by("-id")
        return render(request, self.template_name, {"my_vacancies": my, "active_nav": "profile"})
