from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
  path('', views.welcome, name='welcome'),
  path('home/', views.home, name='home'),
  path('login/', views.login, name='login'),
  path('register/', views.register, name='register'),
  path('profile/<user_id>', views.profile, name='profile'),
  path('explore', views.explore, name='explore'),
  path('profile/<user_id>/edit', views.editpr, name='editpr'),
  path('profile/<user_id>/favorites', views.favorites, name='favorite'),
  path('post/create', views.createPost, name='post.create'),
  path('post/create/search', views.searchSpotify, name='post.create.search'),
  path('post/store', views.storePost, name='post.store')
]