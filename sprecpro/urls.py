from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
  path('', views.welcome, name='welcome'),
  path('home/', views.home, name='home'),
  path('login/', views.login, name='login'),
  path('register/', views.register, name='register'),
  path('profile/<user_id>', views.profile, name='profile'),
  path('profile/edit/<user_id>', views.editpr, name='editpr')
]