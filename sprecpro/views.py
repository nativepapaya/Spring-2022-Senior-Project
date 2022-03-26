from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from .models import *
import requests
import json
import random

def welcome(request):
  return render(request, 'welcome.html', {})

def posts(request):
  return render(request, 'posts.html')

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

def explore(request):
  numbers_list = [None] * 1000
  usernames = ["insidenecktie","winningincomplete","emitbedrock",
              "dangerportfolio","reindeerlittle","negligiblelack",
              "labwould","axelead"]
  for n in range(0,len(numbers_list)-1):
    numbers_list[n] = usernames[random.randint(0, len(usernames)-1)]

  page = request.GET.get('page',1)
  paginator = Paginator(numbers_list, 7)
  try:
    numbers = paginator.page(page)
  except PageNotAnInteger:
    numbers = paginator.page(1)
  except EmptyPage:
    numbers = paginator.page(paginator.num_pages)
  return render(request, 'explore.html', {'numbers': numbers})

def favorites(request, user_id):
  if not request.user.is_authenticated:
    return redirect('login')

  #If not a spotify user (super user), redirect to welcome
  if request.user.is_staff:
    return redirect('welcome')
  
  #The user and profile whos favorites this page belongs to
  profile = Profile.objects.filter(user_id = user_id).first()
  user = User.objects.filter(id = user_id, is_staff = False).first()

  if profile is None or user is None:
    return redirect('welcome')

  return render(request, 'favorites.html', {
    'user': user,
    'profile': profile,
  })
  
def likedSongs(request, user_id):
  user = User.objects.filter(id = user_id, is_staff = False).first()
  playlist_id = "https://open.spotify.com/collection/tracks"
  results = user.user_playlist_tracks(user, playlist_id)
  playlist_items = results['items']
  uris = []
  
  while results['next']:
        results = user.next(results)
        playlist_items.append(results['items'])
  
  for item in playlist_items:
        is_local = item["is_local"]
        if is_local == True:
              continue
        else:
             track_id = item["track"]["uri"]
             uris.append(track_id)
  return render(request, 'favorites.html', {
      'uris' : uris,
    })
  

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
        avatar = getProfilePhoto(request.user)
      )
    
    #get the users most recently played song and set uid field
    song_data = getUserSongData(request.user)
    setattr(profile, 'last_played_uid', song_data['last_played'])
    profile.save()

    #return the view with the user's profile information
    return render(request, 'profile.html', {
      'profile' : profile,
      'top_song': song_data['top_song'],
      'last_played_name': song_data['last_played_name']
    })
  
  #if the user doesn't exist, go back to welcome
  return redirect('welcome')

def editpr(request, user_id):
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

  if user is None:
    return redirect('welcome')
  
  #If someone tries to edit another users edit profile page
  if request.user != user:
    return redirect('welcome')
  
  return render(request, 'editpr.html', {})
  
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
  try:
    photo = data['images'][0]['url']
  except:
    photo = None

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
  try:
    top_song = data['items'][0]['artists'][0]['name'] + ': ' + data['items'][0]['name']
  except:
    top_song = 'Could not find at this time!'
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
  try:
    last_played = data['items'][0]['track']['id']
    last_played_name = data['items'][0]['track']['artists'][0]['name'] + ': ' + data['items'][0]['track']['name']
  except:
    last_played = 'Could not find at this time!'
    last_played_name = 'Could not find at this time!'

  return {
    'top_song' : top_song,
    'last_played': last_played,
    'last_played_name': last_played_name
  }
