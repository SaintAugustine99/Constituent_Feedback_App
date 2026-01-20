from django.urls import path
from .views import CountyListAPI, ConstituencyListAPI, WardListAPI, OfficialListAPI

urlpatterns = [
    path('counties/', CountyListAPI.as_view(), name='county-list'),
    path('constituencies/', ConstituencyListAPI.as_view(), name='constituency-list'),
    path('wards/', WardListAPI.as_view(), name='ward-list'),
    path('officials/', OfficialListAPI.as_view(), name='official-list'),
]
