from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView

from vacancies.models import Vacancy
from vacancies.web_forms import VacancyCreateForm


class SearchView(LoginRequiredMixin, ListView):
    """Страница "Поиск": все вакансии всех пользователей."""

    template_name = "vacancies/search.html"
    context_object_name = "vacancies"
    paginate_by = 10

    def get_queryset(self):
        qs = (
            Vacancy.objects.select_related("user")
            .prefetch_related("skills")
            .order_by("-id")
        )
        q = (self.request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(
                Q(slug__icontains=q)
                | Q(text__icontains=q)
                | Q(user__username__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["active_nav"] = "search"
        ctx["q"] = (self.request.GET.get("q") or "").strip()
        return ctx


class VacancyCreateWebView(LoginRequiredMixin, FormView):
    """Страница "Создать": создание вакансии через HTML-форму."""

    template_name = "vacancies/create.html"
    form_class = VacancyCreateForm
    success_url = reverse_lazy("search")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["active_nav"] = "create"
        return ctx

    def form_valid(self, form):
        vacancy = form.save(commit=False)
        vacancy.user = self.request.user
        vacancy.save()
        form.save_m2m()
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    """Страница "Профиль"."""

    template_name = "vacancies/profile.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["active_nav"] = "profile"
        ctx["my_vacancies"] = (
            Vacancy.objects.filter(user=self.request.user)
            .prefetch_related("skills")
            .order_by("-id")
        )
        return ctx
