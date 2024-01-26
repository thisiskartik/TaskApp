from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet


tasks_router = DefaultRouter()
tasks_router.register('', TaskViewSet, basename="tasks")

urlpatterns = [
    path('', include(tasks_router.urls)),
]
