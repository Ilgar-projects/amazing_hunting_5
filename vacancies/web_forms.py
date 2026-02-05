from django import forms

from vacancies.models import Vacancy, Skill


class VacancyCreateForm(forms.ModelForm):
    """Простая форма создания вакансии для веб-интерфейса."""

    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.filter(is_active=True),
        required=False,
        label="Навыки",
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Vacancy
        fields = ("slug", "text", "min_experience", "status", "skills")
        labels = {
            "slug": "Название / заголовок",
            "text": "Описание",
            "min_experience": "Мин. опыт (лет)",
            "status": "Статус",
        }
        widgets = {
            "slug": forms.TextInput(attrs={"placeholder": "Например: Курьер в доставку"}),
            "text": forms.Textarea(attrs={"rows": 6, "placeholder": "Коротко опишите вакансию..."}),
            "min_experience": forms.NumberInput(attrs={"min": 0, "step": 1, "placeholder": "0"}),
        }
