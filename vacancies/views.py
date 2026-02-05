from django.db.models import Q, F
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

import vacancies
from vacancies.models import Vacancy, Skill
from vacancies.permissions import VacancyCreatePermissions
from vacancies.serializers import VacancyListSerializer, VacancyDetailSerializer, VacancyCreateSerializer, \
    VacancyUpdateSerializer, VacancyDestroySerializer, SkillSerializer


def hello(request):
    return HttpResponse('''
    <!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Регистрация</title>
  <style>
    body{font-family:system-ui,Segoe UI,Arial; background:#08141b; color:#e8f3ff; margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;}
    .card{width:min(420px,92vw); background:rgba(255,255,255,.06); border:1px solid rgba(255,255,255,.10); border-radius:18px; padding:22px; box-shadow:0 20px 60px rgba(0,0,0,.35);}
    h1{margin:0 0 6px; font-size:22px;}
    p{margin:0 0 18px; opacity:.8;}
    label{display:block; margin:10px 0 6px; opacity:.9;}
    input{width:100%; padding:12px 12px; border-radius:12px; border:1px solid rgba(255,255,255,.14); background:rgba(0,0,0,.25); color:#e8f3ff;}
    .btn{width:100%; margin-top:14px; padding:12px; border-radius:14px; border:0; background:#2aa7ff; color:#06202b; font-weight:700; cursor:pointer;}
    .err{margin-top:10px; color:#ffb4b4;}
    .link{margin-top:14px; text-align:center; opacity:.9;}
    a{color:#7fd7ff; text-decoration:none;}
  </style>
</head>
<body>
  <div class="card">
    <h1>Создать аккаунт</h1>
    <p>Регистрация займет минуту.</p>

    <form method="post">
      {% csrf_token %}

      {{ form.non_field_errors }}

      <label for="id_username">Имя пользователя</label>
      {{ form.username }}
      <div class="err">{{ form.username.errors }}</div>

      <label for="id_email">Email</label>
      {{ form.email }}
      <div class="err">{{ form.email.errors }}</div>

      <label for="id_password1">Пароль</label>
      {{ form.password1 }}
      <div class="err">{{ form.password1.errors }}</div>

      <label for="id_password2">Повтор пароля</label>
      {{ form.password2 }}
      <div class="err">{{ form.password2.errors }}</div>

      <button class="btn" type="submit">Зарегистрироваться</button>
    </form>

    <div class="link">
      Уже есть аккаунт? <a href="{% url 'login' %}">Войти</a>
    </div>
  </div>
</body>
</html>

    ''')


class SkillsViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class VacancyListView(ListAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyListSerializer

    def get(self, request, *args, **kwargs):
        vacancy_text = request.GET.get('text', None)
        if vacancy_text:
            self.queryset = self.queryset.filter(
                text__icontains=vacancy_text
            )
        skills = request.GET.getlist("skill", None)
        skills_q = None
        for skill in skills:
            if skills_q is None:
                skills_q = Q(skills__name__icontains=skill)
            else:
                skills_q |= Q(skills__name__icontains=skill)
        if skills_q:
            self.queryset = self.queryset.filter(skills_q)

        return super().get(request, *args, **kwargs)

        # skill_name = request.GET.get("skill", None)
        # if skill_name:
        #     self.queryset = self.queryset.filter(
        #         skills__name__icontains=skill_name
        #     )
        # return super().get(request, *args, **kwargs)

        # return Response({"message": "Хаха я переопределил вот так этот метод"})


class VacancyDetailView(RetrieveAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer
    permission_classes = [IsAuthenticated]


class VacancyCreateView(CreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer
    permission_classes = [IsAuthenticated]


class VacancyUpdateView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer


class VacancyDeleteView(DestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDestroySerializer


class VacancyLikeView(UpdateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyDetailSerializer

    def put(self, request, *args, **kwargs):
        Vacancy.objects.filter(pk__in=request.data).update(likes=F('likes') + 1)

        return JsonResponse(
            VacancyDetailSerializer(Vacancy.objects.filter(pk__in=request.data), many=True).data,
            safe=False
        )


class UserVacancyDetailView():
    pass

# следующая тема 30.2.2
