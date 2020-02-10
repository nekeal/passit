from rest_framework import viewsets

from news.models import News
from news.serializers import NewsBaseSerializer


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = NewsBaseSerializer
    queryset = News.objects.all()
