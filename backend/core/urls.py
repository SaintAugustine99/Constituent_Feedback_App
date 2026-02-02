from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
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
    path('api/issues/', include('issues.urls')),
    path('api/facilities/', include('facilities.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/locations/', include('locations.urls')),  # For officials endpoint
    path('api/news/', include('news.urls')),
    path('api/assistant/', include('assistant.urls')),
]

# Serve media files in all environments (demo deployment)
# For production at scale, use S3/CloudFront instead
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
