from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
  path('', views.welcome, name='welcome'),
  path('home/', views.home, name='home'),
  path('explore', views.explore, name='explore'),

  path('login/', views.login, name='login'),
  path('profile/<user_id>', views.profile, name='profile'),
  path('profile/<user_id>/edit', views.editpr, name='editpr'),
  path('profile/<user_id>/update', views.updateProfile, name="updateProfile"),
  path('profile/<user_id>/search', views.searchForFeatured, name="searchForFeatured"),
  path('follow/<user_id>', views.follow, name='follow'),
  path('unfollow/<user_id>', views.unfollow, name='unfollow'),
 
  path('profile/<user_id>/favorites', views.favorites, name='favorite'),
  path('favorites/searchFor', views.searchForFavorites, name='search_for_favorites'),
  path('fav/', views.addToFavorites, name='add_fav'),
  path('nofav/<id>', views.deleteFromFavorites, name='delete_fav'),

  path('post/create', views.createPost, name='post.create'),
  path('post/create/search', views.searchSpotify, name='post.create.search'),
  path('post/store', views.storePost, name='post.store'),
  path('post/<pk>', views.viewPost, name='post.view'),
  path('post/<post_id>/edit', views.editPost, name='post.edit'),
  path('post/<post_id>/delete', views.deletePost, name='post.delete'),
  path('like/<pk>', views.likePost, name='like_post'),
  path('unlike/<pk>', views.unlikePost, name='unlike_post'),
  path('comment/<pk>', views.comment, name='comment'),
  path('comment/<pk>/delete', views.deleteComment, name='comment.delete'),
]