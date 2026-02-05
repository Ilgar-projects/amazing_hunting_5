from __future__ import annotations

from django import forms
from django.utils.text import slugify

from vacancies.models import Vacancy, Skill


class VacancyWebForm(forms.ModelForm):
    # можно ввести свои навыки: "python, docker, linux"
    custom_skills = forms.CharField(
        required=False,
        label="Свои навыки (необязательно)",
        help_text="Можно через запятую или с новой строки",
        widget=forms.TextInput(attrs={"placeholder": "например: python, docker, linux"}),
    )

    class Meta:
        model = Vacancy
        fields = ("title", "text", "min_experience", "status", "skills")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Например: Работа с бетоном"}),
            "text": forms.Textarea(attrs={"rows": 5, "placeholder": "Опиши вакансию..."}),
            "min_experience": forms.NumberInput(attrs={"min": 0}),
        }

    def clean_title(self):
        title = (self.cleaned_data.get("title") or "").strip()
        if not title:
            raise forms.ValidationError("Укажи название вакансии.")
        return title

    def clean(self):
        cleaned = super().clean()
        # гарантируем, что slug можно построить (на всякий случай)
        title = cleaned.get("title") or ""
        if title:
            cleaned["slug"] = slugify(title, allow_unicode=True)[:140] or "vacancy"
        return cleaned

    def save(self, user=None, commit=True):
        vacancy: Vacancy = super().save(commit=False)
        if user is not None:
            vacancy.user = user
        if commit:
            vacancy.save()
            self.save_m2m()
            self._apply_custom_skills(vacancy)
        return vacancy

    def _apply_custom_skills(self, vacancy: Vacancy) -> None:
        raw = (self.cleaned_data.get("custom_skills") or "").strip()
        if not raw:
            return

        parts = []
        for chunk in raw.replace("\n", ",").split(","):
            name = chunk.strip()
            if name:
                parts.append(name[:20])  # Skill.name max_length=20

        for name in parts:
            skill_obj, _ = Skill.objects.get_or_create(name=name)
            vacancy.skills.add(skill_obj)
