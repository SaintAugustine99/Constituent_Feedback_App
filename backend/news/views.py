from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import GovernmentResource, NewsArticle
from .serializers import GovernmentResourceSerializer, NewsArticleSerializer


class GovernmentResourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GovernmentResource.objects.all()
    serializer_class = GovernmentResourceSerializer
    permission_classes = [AllowAny]


class NewsArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsArticle.objects.all()
    serializer_class = NewsArticleSerializer
    permission_classes = [AllowAny]
