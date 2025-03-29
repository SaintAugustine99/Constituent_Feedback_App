# accounts/web_urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import web_views

urlpatterns = [
    path('login/', web_views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', web_views.register_view, name='register'),
    path('profile/', web_views.profile_view, name='profile'),
    path('profile/edit/', web_views.edit_profile_view, name='edit_profile'),
]