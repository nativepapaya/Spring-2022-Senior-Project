from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import *
from .models import *
import requests
import json

def welcome(request):
  return render(request, 'welcome.html', {})

def home(request):
  if not request.user.is_authenticated: 
    return redirect('welcome')

  return render(request, 'home.html', {})

def profile(request, user_id):
  #If the user is not logged in
  if not request.user.is_authenticated:
    return redirect('login')

  #If not a spotify user, return back to welcome
  if request.user.is_staff:
    return redirect('welcome')

  #Find the user's profile who's id matches the passed id in the route
  #Find the user whos's id was passed in the route, validate they arent staff
  profile = Profile.objects.filter(user_id = user_id).first()
  user = User.objects.filter(id = user_id, is_staff = False).first()

  #If there is no profile and the user exists, create a profile
  if user is not None:
    if profile is None:
      Profile.objects.create(
        user_id = request.user,
        avatar = getProfilePhoto(request.user),
      )
    #return the view with the user's profile information
    return render(request, 'profile.html', {'profile' : profile})
  
  #if the user doesn't exist, go back to welcome
  return redirect('welcome')
  
  
def getProfilePhoto(user):
  spotify_id = user.social_auth.get(provider='spotify').uid
  social = user.social_auth.get(provider='spotify')
  token = social.extra_data['access_token']
  
  response = requests.get(
    url = "https://api.spotify.com/v1/users/"+spotify_id, 
    headers = {
      'Authorization': 'Bearer ' + token
    }
  )
  text = response.text
  data = json.loads(text)

  photo = data['images'][0]['url']
  return photo