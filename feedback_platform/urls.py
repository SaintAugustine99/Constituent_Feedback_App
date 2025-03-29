"""
URL configuration for feedback_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view

def welcome_view(request):
    return JsonResponse({
        "message": "Welcome to the Constituent Feedback Platform API",
        "endpoints": {
            "admin": "/admin/",
            "api": "/api/"
        }
    })


urlpatterns = [
    path('', home_view, name='home'), 
    path('admin/', admin.site.urls),

 # API endpoints
    path('api/home/', home_view, name='home'),
    path('api/', include('accounts.urls')),
    path('api/', include('feedback.urls')),
    path('api/', include('publications.urls')),
    path('api/', include('complaints.urls')),
    path('api/', include('search.urls')),
    path('api/', include('analytics.urls')),

# HTML template views (to be implemented in each app)
    path('accounts/', include('accounts.web_urls')),
    path('feedback/', include('feedback.web_urls')),
    path('complaints/', include('complaints.web_urls')),
    path('publications/', include('publications.web_urls')),
    path('analytics/', include('analytics.web_urls')),
    path('search/', include('search.web_urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
