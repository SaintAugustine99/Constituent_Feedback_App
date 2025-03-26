# accounts/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserProfileView, DistrictListView

urlpatterns = [
    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/profile/', UserProfileView.as_view(), name='profile'),
    path('districts/', DistrictListView.as_view(), name='district-list'),
]

# feedback_platform/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
]