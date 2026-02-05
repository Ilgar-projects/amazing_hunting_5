from django.db import migrations, models
from django.db.models import F


def forwards_fill_title(apps, schema_editor):
    Vacancy = apps.get_model("vacancies", "Vacancy")
    Vacancy.objects.filter(title="").update(title=F("slug"))


class Migration(migrations.Migration):

    dependencies = [
        ("vacancies", "0009_alter_vacancy_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="vacancy",
            name="title",
            field=models.CharField(blank=True, default="", max_length=120, verbose_name="Название / заголовок"),
        ),
        migrations.AlterField(
            model_name="vacancy",
            name="slug",
            field=models.SlugField(allow_unicode=True, blank=True, max_length=140),
        ),
        migrations.AlterField(
            model_name="vacancy",
            name="text",
            field=models.CharField(max_length=2000, verbose_name="Описание"),
        ),
        migrations.AlterField(
            model_name="vacancy",
            name="skills",
            field=models.ManyToManyField(blank=True, to="vacancies.skill"),
        ),
        migrations.RunPython(forwards_fill_title, migrations.RunPython.noop),
    ]
