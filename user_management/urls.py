from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Login, Register, Profile, ProfileDetail

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('profile/', Profile.as_view()),
    path('profile/detail/', ProfileDetail.as_view())
]