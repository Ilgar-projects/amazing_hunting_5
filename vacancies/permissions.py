from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission

from authentication.models import User


class VacancyCreatePermissions(BasePermission):
    message = "Добавление вакансии для не HR запрещено"

    def has_permission(self, request, view):
        if request.user.role == User.HR:
            return True
        return False
