from tkinter import CASCADE
from django.conf import settings
from django.db import models
class Profile(models.Model):
  id = models.AutoField(primary_key=True)
  user_id = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE #on user deletion, profile will cascade delete
  )
  avatar = models.TextField(null=True)
  pronouns = models.CharField(
    max_length=9, 
    choices=[('he/him', 'he/him'), ('she/her', 'she/her'), ('they/them', 'they/them')],
    null=True
  )
  age = models.IntegerField(null=True)
  bio = models.TextField(max_length=100, null=True)
  last_played_uid = models.TextField(null=True) #represents the id of the last spotify track played
  created_at = models.DateTimeField(auto_now_add=True),
  updated_at = models.DateTimeField(auto_now=True),

  def getId(self):
    return self.id
  
  def getAvatar(self):
    return self.avatar

class Favorite(models.Model):
  id = models.AutoField(primary_key=True)
  user_id = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE #on user deletion, profile will cascade delete
  )
  last_played_uid = models.TextField(null=True) #represents the id of the last spotify track played
  created_at = models.DateTimeField(auto_now_add=True)
  edited_at = models.DateTimeField(auto_now=True)
  
  def getFavID(self):
    return self.fav_id

class Post(models.Model):
  id = models.AutoField(primary_key=True)
  user_id = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
  )
  profile = models.ForeignKey(
    Profile,
    on_delete=models.CASCADE
  )
  title = models.TextField(null=False, max_length=100)
  description = models.TextField(null=True, max_length=240)
  rec_song_id = models.TextField(null=True)
  rec_album_id = models.TextField(null=True)
  created_at = models.DateTimeField(auto_now_add=True),
  updated_at = models.DateTimeField(auto_now=True),

class Like(models.Model):
  id = models.AutoField(primary_key=True)
  user_id = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
  )
  post_id = models.ForeignKey(
    Post,
    on_delete=models.CASCADE
  )
  like_type = models.CharField(
    max_length=7,
    choices=[('Like', 'Like'), ('Dislike', 'Dislike')],
    null=False
  )
  created_at = models.DateTimeField(auto_now_add=True),
  updated_at = models.DateTimeField(auto_now=True),

class Comment(models.Model):
  id = models.AutoField(primary_key=True)
  user_id = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
  )
  post_id = models.ForeignKey(
    Post,
    on_delete=models.CASCADE
  )
  body = models.TextField(null=False, max_length=240)
  created_at = models.DateTimeField(auto_now_add=True),
  updated_at = models.DateTimeField(auto_now=True),

class Follow(models.Model):
  id = models.AutoField(primary_key=True)
  follower_id = models.ForeignKey( #The user who clicked the Follow Button
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='follower_id'
  )
  followee_id = models.ForeignKey( #The user who was Followed
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name='followee_id'
  )
  created_at = models.DateTimeField(auto_now_add=True),
  updated_at = models.DateTimeField(auto_now=True),
