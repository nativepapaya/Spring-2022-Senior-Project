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
