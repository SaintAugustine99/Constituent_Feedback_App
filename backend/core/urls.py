from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from locations.views import CountyListAPI, ConstituencyListAPI, WardListAPI
from accounts.views import RegisterView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- Auth Endpoints ---
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    
    # --- Location Data Endpoints (For the Dropdowns) ---
    path('api/counties/', CountyListAPI.as_view(), name='counties'),
    path('api/constituencies/', ConstituencyListAPI.as_view(), name='constituencies'), # Usage: ?county_id=1
    path('api/wards/', WardListAPI.as_view(), name='wards'), # Usage: ?constituency_id=5

    # --- Legislative Tracker ---
    path('api/legislation/', include('legislative_tracker.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

