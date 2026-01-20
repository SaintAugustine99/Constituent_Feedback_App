from django.urls import path
from .views import ProjectList, ProjectDetail, ProjectUpdateListCreate

urlpatterns = [
    path('', ProjectList.as_view(), name='project-list'),
    path('<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    path('updates/', ProjectUpdateListCreate.as_view(), name='project-updates'),
]
