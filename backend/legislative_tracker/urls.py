from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LegalInstrumentViewSet, FeedbackViewSet, DocketViewSet

router = DefaultRouter()
router.register(r'instruments', LegalInstrumentViewSet)
router.register(r'feedback', FeedbackViewSet)
router.register(r'dockets', DocketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
