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

def welcome_view(request):
    return JsonResponse({
        "message": "Welcome to the Constituent Feedback Platform API",
        "endpoints": {
            "admin": "/admin/",
            "api": "/api/"
        }
    })


urlpatterns = [
    path('', welcome_view, name='welcome'), 
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('feedback.urls')),
    path('api/', include('publications.urls')),
    path('api/', include('complaints.urls')),
    path('api/', include('search.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
