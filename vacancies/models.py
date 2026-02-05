from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.text import slugify

from authentication.models import User


def check_date_not_past(value: date):
    if value < date.today():
        raise ValidationError(f"{value} это же прошлое!)))")


class Skill(models.Model):
    name = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"

    def __str__(self):
        return self.name


class Vacancy(models.Model):
    STATUS = [
        ("draft", "Черновик"),
        ("open", "Открыта"),
        ("closed", "Закрыта")
    ]

    # То, что видит пользователь (можно кириллицу/пробелы)
    title = models.CharField(max_length=120, blank=True, default="", verbose_name="Название / заголовок")

    # Служебное поле (для красивых URL/идентификаторов). Разрешаем Unicode.
    slug = models.SlugField(max_length=140, allow_unicode=True, blank=True)

    text = models.CharField(max_length=2000, verbose_name="Описание")
    status = models.CharField(max_length=6, choices=STATUS, default="draft")
    created = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    likes = models.IntegerField(default=0)
    min_experience = models.IntegerField(null=True, validators=[MinValueValidator(0)])
    updated_at = models.DateField(null=True, validators=[check_date_not_past])

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ["id"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Автоматически делаем slug из title (включая кириллицу).
        if not self.slug and self.title:
            base = slugify(self.title, allow_unicode=True)[:120] or "vacancy"
            candidate = base
            n = 1
            while Vacancy.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                n += 1
                candidate = f"{base}-{n}"
                if len(candidate) > 140:
                    candidate = candidate[:140]
            self.slug = candidate
        super().save(*args, **kwargs)

    @property
    def username(self):
        return self.user.username if self.user else None
