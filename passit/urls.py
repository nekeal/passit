from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter

from .events.urls import router as events_router
from .lecturers.urls import router as lecturers_router
from .news.urls import router as news_router
from .subject.urls import router as subject_router
from .views import index

schema_view = get_schema_view(
    openapi.Info(
        title="Passit API",
        default_version="v1",
        description="API passit wiki",
        license=openapi.License(name="GNU General Public License v3.0"),
    ),
    authentication_classes=(SessionAuthentication,),
    permission_classes=(AllowAny,),
)


router = DefaultRouter()

router.registry.extend(subject_router.registry)
router.registry.extend(lecturers_router.registry)
router.registry.extend(news_router.registry)
router.registry.extend(events_router.registry)

urlpatterns = [
    path("", index),
    path("api/", include((router.urls, "api"))),
    path("api/auth/", include("passit.accounts.urls")),
    path("admin/", admin.site.urls),
    path("docs/", schema_view.with_ui("redoc")),
]
if settings.DEBUG:  # pragma: no cover
    urlpatterns.append(path("silk/", include("silk.urls", namespace="silk")))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns.append(re_path(r"^.*/$", index))
