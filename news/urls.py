from typing import List, Any

from rest_framework.routers import DefaultRouter

from news.views import NewsViewSet

router = DefaultRouter()

router.register('news', NewsViewSet)
urlpatterns: List[Any] = [

]

urlpatterns += router.urls
