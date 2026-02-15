"""
URL configuration for amazing_hunting_5 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.templatetags.static import static as staticfiles_static
from rest_framework import routers

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.contrib.auth.views import LogoutView

from authentication.web_views import AuthLandingView
from vacancies.web_views import SearchView, VacancyCreateWebView, ProfileView
from vacancies.views import SkillsViewSet

router = routers.SimpleRouter()
router.register('skill', SkillsViewSet)

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_static('favicon/favicon.ico'), permanent=True)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', SearchView.as_view(), name='home'),
    path('auth/', AuthLandingView.as_view(), name='auth'),
    path('search/', SearchView.as_view(), name='search'),
    path('create/', VacancyCreateWebView.as_view(), name='create'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('vacancy/', include('vacancies.urls')),
    path('company/', include('companies.urls')),
    path('user/', include('authentication.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
