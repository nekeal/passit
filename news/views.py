from rest_framework import viewsets

from news.models import News
from news.serializers import NewsListSerializer


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsListSerializer
    queryset = News.objects.all()
