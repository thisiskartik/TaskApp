from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from .views import register, user, login, token


urlpatterns = [
    path('', user),
    path('register/', register),
    path('login/', login),
    path('token/', token),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/revoke/', TokenBlacklistView.as_view()),
]
