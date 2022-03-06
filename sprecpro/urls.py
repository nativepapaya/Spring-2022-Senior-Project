from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
  path('', views.welcome, name='welcome'),
  path('home/', views.home, name='home'),
  path('profile/<user_id>', views.profile, name='profile')
]