from rest_framework.routers import DefaultRouter
from .views import GovernmentResourceViewSet, NewsArticleViewSet

router = DefaultRouter()
router.register('resources', GovernmentResourceViewSet)
router.register('articles', NewsArticleViewSet)

urlpatterns = router.urls
