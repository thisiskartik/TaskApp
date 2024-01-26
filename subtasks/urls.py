from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubTaskViewSet


subtasks_router = DefaultRouter()
subtasks_router.register('', SubTaskViewSet, basename='subtasks')

urlpatterns = [
    path('', include(subtasks_router.urls)),
]
