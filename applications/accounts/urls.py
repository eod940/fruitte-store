from django.urls import path

from applications.accounts.views import JwtRegisterAPIView

urlpatterns = [
    path('register/', JwtRegisterAPIView.as_view()),
]