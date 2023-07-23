from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/',views.UserLoginView.as_view(),name='login'),
    path('profile/',views.UserProfileView.as_view(), name='profile'),
    path('changepassword/',views.UserChangePassword.as_view(), name='changepassword'),
]
