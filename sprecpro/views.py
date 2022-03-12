from django.contrib.auth.models import User
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
    return redirect('login')
  
  if request.user.is_staff:
    return redirect('welcome')

  return render(request, 'home.html', {})

def login(request):
  return render(request, 'login_page.html', {})

def register(request):
  return render(request, 'register_page.html', {})

#------------------------------------
def favorites(request):
  if not request.user.is_authenticated:
    return redirect('login')

  #If not a spotify user (super user), redirect to welcome
  if request.user.is_staff:
    return render(request, 'favorites.html', {})
#------------------------------------------

def profile(request, user_id):
  #If the user is not logged in
  if not request.user.is_authenticated:
    return redirect('login')

  #If not a spotify user (super user), redirect to welcome
  if request.user.is_staff:
    return redirect('welcome')

  #Find the user's profile who's id matches the passed id in the route
  #Find the user whos's id was passed in the route, and validate they arent a super user
  profile = Profile.objects.filter(user_id = user_id).first()
  user = User.objects.filter(id = user_id, is_staff = False).first()

  #If there is no profile and the user exists, create a profile
  if user is not None:
    if profile is None:
      Profile.objects.create(
        user_id = request.user,
        avatar = getProfilePhoto(request.user),
      )
    
    #get the users most recently played song and set uid field
    #song_data = getUserSongData(request.user)
    #setattr(profile, 'last_played_uid', song_data['last_played'])
    #profile.save()

    #return the view with the user's profile information
    return render(request, 'profile.html', {
      'profile' : profile,
      #'top_song': song_data['top_song']
    })
  
  #if the user doesn't exist, go back to welcome
  return redirect('welcome')
  
def getProfilePhoto(user):
  #access the users spotify id and access token
  spotify_id = user.social_auth.get(provider='spotify').uid
  social = user.social_auth.get(provider='spotify')
  token = social.extra_data['access_token']
  
  #send the request to the spotify api on behalf of the user
  response = requests.get(
    url = "https://api.spotify.com/v1/users/"+spotify_id, 
    headers = {
      'Authorization': 'Bearer ' + token
    }
  )

  text = response.text
  data = json.loads(text)

  #parse the results and return the users photo
  photo = data['images'][0]['url']
  return photo

def getUserSongData(user):
  #Get the "social user" and their spoitfy access token
  social = user.social_auth.get(provider='spotify')
  token = social.extra_data['access_token']

  #sends a request to the endpoint with the filters for getting the users top song
  response = requests.get(
    url = "	https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=1",
    headers = {
      'Authorization': 'Bearer ' + token
    },
  )
  text = response.text
  data = json.loads(text)

  #parses the json data and stores the top song
  top_song = data['items'][0]['artists'][0]['name'] + ', ' + data['items'][0]['name']

  #sends a request to the endpoint with filters for getting the users most recently listened to song
  response = requests.get(
    url = "	https://api.spotify.com/v1/me/player/recently-played?limit=1",
    headers = {
      'Authorization': 'Bearer ' + token
    }
  )

  text = response.text
  data = json.loads(text)

  #parses the data and stores the last played song
  last_played = data['items'][0]['track']['id']

  return {
    'top_song' : top_song,
    'last_played': last_played
  }