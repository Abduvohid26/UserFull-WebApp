from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.RegisterAPIView.as_view()),
    path('signin/', views.LoginAPIView.as_view()),
]