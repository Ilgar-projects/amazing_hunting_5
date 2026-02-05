from django.utils.text import slugify
from rest_framework import serializers

from vacancies.models import Vacancy, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class VacancyListSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Vacancy
        fields = ["id", "title", "text", "slug", "status", "created", "username", "skills", "min_experience", "likes"]


class VacancyDetailSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    class Meta:
        model = Vacancy
        fields = "__all__"


class VacancyCreateSerializer(serializers.ModelSerializer):
    """
    Создание вакансии.
    - title: можно писать кириллицей и с пробелами
    - slug: необязательный (если не задан — будет сделан автоматически из title)
    - skills: список строк; если навыка нет — создадим
    """
    id = serializers.IntegerField(required=False)

    title = serializers.CharField(max_length=120, required=True)

    slug = serializers.CharField(max_length=140, required=False, allow_blank=True)

    skills = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Skill.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = Vacancy
        fields = "__all__"

    def is_valid(self, raise_exception=False):
        self._skills = self.initial_data.pop("skills", [])
        return super().is_valid(raise_exception=raise_exception)

    def validate(self, attrs):
        title = (attrs.get("title") or "").strip()
        raw_slug = (attrs.get("slug") or "").strip()

        if not title and not raw_slug:
            raise serializers.ValidationError({"title": "Укажи название (title) или slug."})

        # если title пустой — возьмём из slug (обратная совместимость)
        if not title and raw_slug:
            title = raw_slug

        # slug делаем из title (Unicode slug)
        computed = slugify(raw_slug or title, allow_unicode=True)[:140] or "vacancy"

        # чуть-чуть гарантируем уникальность на уровне приложения
        base = computed
        n = 1
        while Vacancy.objects.filter(slug=computed).exists():
            n += 1
            computed = f"{base}-{n}"
            if len(computed) > 140:
                computed = computed[:140]

        attrs["title"] = title
        attrs["slug"] = computed
        return attrs

    def create(self, validated_data):
        vacancy = Vacancy.objects.create(**validated_data)

        for skill in self._skills:
            skill_obj, _ = Skill.objects.get_or_create(name=skill)
            vacancy.skills.add(skill_obj)
        vacancy.save()
        return vacancy


class VacancyUpdateSerializer(serializers.ModelSerializer):
    skills = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Skill.objects.all(),
        slug_field="name"
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateField(read_only=True)

    title = serializers.CharField(max_length=120, required=False)

    slug = serializers.CharField(max_length=140, required=False, allow_blank=True)

    class Meta:
        model = Vacancy
        fields = ["id", "title", "text", "status", "slug", "user", "created", "skills"]

    def is_valid(self, raise_exception=False):
        self._skills = self.initial_data.pop("skills", [])
        return super().is_valid(raise_exception=raise_exception)

    def validate(self, attrs):
        title = (attrs.get("title") or "").strip()
        raw_slug = (attrs.get("slug") or "").strip()

        if raw_slug or title:
            computed = slugify(raw_slug or title, allow_unicode=True)[:140] or "vacancy"
            base = computed
            n = 1
            qs = Vacancy.objects.all()
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            while qs.filter(slug=computed).exists():
                n += 1
                computed = f"{base}-{n}"
                if len(computed) > 140:
                    computed = computed[:140]
            attrs["slug"] = computed
        return attrs

    def save(self):
        vacancy = super().save()

        for skill in self._skills:
            skill_obj, _ = Skill.objects.get_or_create(name=skill)
            vacancy.skills.add(skill_obj)
        vacancy.save()
        return vacancy


class VacancyDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = ["id"]
