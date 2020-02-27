"""teleagh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter

from subject.urls import router as subject_router
from lecturers.urls import router as lecturers_router
from news.urls import router as news_router


schema_view = get_schema_view(openapi.Info(
    title='Passit API',
    default_version='v1',
    description='API passit wiki',
    license=openapi.License(name='GNU General Public License v3.0'),
),
    authentication_classes=(SessionAuthentication, ),
    permission_classes=(AllowAny,)
)


router = DefaultRouter()

router.registry.extend(subject_router.registry)
router.registry.extend(lecturers_router.registry)
router.registry.extend(news_router.registry)

urlpatterns = [
    path('', RedirectView.as_view(url='/api')),
    path('api/', include((router.urls, 'api'))),
    path('api/auth/', include('accounts.urls')),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('redoc')),
]
