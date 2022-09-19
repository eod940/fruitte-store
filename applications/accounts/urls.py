from django.urls import path

from applications.accounts.views import JwtRegisterAPIView, JwtLoginView, JwtLogoutView

urlpatterns = [
    path('register/', JwtRegisterAPIView.as_view()),
    path('auth/', JwtLoginView.as_view()),
    path('de-auth/', JwtLogoutView.as_view()),
]