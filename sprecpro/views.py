from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from .models import *
import requests
import json
import random

def welcome(request):
  return render(request, 'welcome.html', {})

def login(request):
  return render(request, 'login_page.html', {})

def register(request):
  return render(request, 'register_page.html', {})

def explore(request):
  posts_list = Post.objects.all()
  page = request.GET.get('page',1)
  paginator = Paginator(posts_list, 7)

  try:
    posts = paginator.page(page)
  except PageNotAnInteger:
    posts = paginator.page(1)
  except EmptyPage:
    posts = paginator.page(paginator.num_pages)
  return render(request, 'explore.html', {'posts': posts})

##################################
#FAVORITES
##################################

#favorite
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

  display_all_favorites = Favorite.objects.filter(user_id=user)

  return render(request, 'favorites.html', {
    'user': user,
    'profile': profile,
    'favorites': display_all_favorites,
  })
  
def likedSongs(request, user_id):
  user = User.objects.filter(id = user_id, is_staff = False).first()
  playlist_id = "37i9dQZF1EUMDoJuT8yJsl"
  songs = request.playlist(playlist_id, fields=None, market=None, additional_types=('track',))
  return render(request, 'favorites.html', {
    'songs' : songs,
  })


#-------------------------------  
  

#search_for_favorites
def searchForFavorites(request):
  if not request.user.is_authenticated: 
    return redirect('login')

  #Validate the inputs
  song_name = request.GET['song_name']
  artist_name = request.GET['artist_name']  
  query_string = song_name + " " + artist_name
  limit = '5'

  social = request.user.social_auth.get(provider='spotify')
  token = social.extra_data['access_token']

  response = requests.get(
    url = 'https://api.spotify.com/v1/search?q='+query_string+'&type=track&market=ES&limit='+limit,
    headers = {
      'Authorization': 'Bearer ' + token
    }
  )
  
  text = response.text
  data = json.loads(text)

  #Check to see if response has a 401 error (token expired). If it does it will alert the user. 
  try:
    if data['error']['status'] == 401:
      messages.error(request, 'Your access token has expired. Please re-login')
      return redirect('welcome')
  except:
    print("Request success")

  songs = {}
  loop = data['tracks']['total']
  if (data['tracks']['total'] > data['tracks']['limit']):
    loop = data['tracks']['limit']
  
  for i in range(0,loop):
    song_id = data['tracks']['items'][i]['id']
    song_name = data['tracks']['items'][i]['name']

    songs[i] = {
      'song_id': song_id,
      'song_name': song_name
    }

  user = request.user
  profile = Profile.objects.filter(user_id = user).first()
  display_all_favorites = Favorite.objects.filter(user_id=user)

  print(songs.values())

  #Return back to the same page with the now queried song Data!
  return render(request, 'favorites.html', {
    'songs': songs.values(),
    'profile': profile,
    'favorites': display_all_favorites
  })

#add_fav
def addToFavorites(request):
  if not request.user.is_authenticated: 
    return redirect('login')

  user = request.user
  song_uid = request.GET['song_id']
  song = request.GET['song_name']
  
  #If the song_uid already exists in the user's Favorites,
  #then the song will not be added
  if Favorite.objects.filter(user_id = user, song_uid = song_uid).first() == None:
    favorited = Favorite.objects.create(
      user_id = user,
      song_uid = song_uid,
      song_name = song
    )
    favorited.save()
  
  #Keeps the user on the same page where the request was made
  user = request.user
  profile = Profile.objects.filter(user_id = user).first()
  display_all_favorites = Favorite.objects.filter(user_id=user)

  return render(request, 'favorites.html', {
    'user': user,
    'profile': profile,
    'favorites': display_all_favorites,
  })

#delete_fav
def deleteFromFavorites(request, id):

  #If the passed-in ID exists in the Favorite table,
  #get the item that has that ID and put it in a variable
  favorited = Favorite.objects.filter(id = id).first()

  #Delete it since that item exists
  if favorited != None:
    favorited.delete()

  #Keeps the user on the same page where the request was made
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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
    if not song_data['last_played'] == None or song_data['last_played'] == '':
      #setattr(profile, 'last_played_uid', song_data['last_played'])
      profile.save()
    
    user_posts = Post.objects.filter(user_id = user_id)

    #return the view with the user's profile information
    return render(request, 'profile.html', {
      'posts': user_posts,
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

##################################
#Search for a Song via SONG NAME and ARTIST NAME
#Searching for a Song via this also returns its ALBUM
##################################

def searchSpotify(request):
  if not request.user.is_authenticated: 
    return redirect('login')

  #handle amount of tracks to query based on where the request is coming from
  if request.path == '/post/create/search':
    limit = '1' #Limit to 1 track returned
  else:
    limit = '10'

  #Validate the inputs
  song_name = request.GET['song_name']
  artist_name = request.GET['artist_name']  
  query_string = song_name + " " + artist_name

  social = request.user.social_auth.get(provider='spotify')
  token = social.extra_data['access_token']
  print('https://api.spotify.com/v1/search?q='+query_string+'&type=track&market=ES&limit='+limit)

  response = requests.get(
    url = 'https://api.spotify.com/v1/search?q='+query_string+'&type=track&market=ES&limit='+limit,
    headers = {
      'Authorization': 'Bearer ' + token
    }
  )
  
  text = response.text
  data = json.loads(text)

  #Check to see if response has a 401 error (token expired). If it does it will alert the user. 
  try:
    if data['error']['status'] == 401:
      messages.error(request, 'Your access token has expired. Please re-login')
      return redirect('welcome')
  except:
    print("Request success")

  returned_main_artist_name = data['tracks']['items'][0]['artists'][0]['name']
  returned_song_name = data['tracks']['items'][0]['name']
  returned_song_id = data['tracks']['items'][0]['id']
  returned_album_name = data['tracks']['items'][0]['album']['name']
  returned_album_id = data['tracks']['items'][0]['album']['id']

  #debug info
  print(
    "Artist Name: " + returned_main_artist_name + "\n" +
    "Song Name: " + returned_song_name + "\n" +
    "Song Id: " + returned_song_id + "\n" +
    "Album Id: " + returned_album_id + "\n" +
    "Album Name: " + returned_album_name + "\n"
  )
  
  #Return back to the same page with the now queried song Data!
  return render(request, 'posts/create_post.html', {
    'song_name' : returned_song_name,
    'song_id': returned_song_id,
    'artist_name': returned_main_artist_name,
    'album_name': returned_album_name,
    'album_id': returned_album_id
  })


##################################
#POSTS
##################################

#Posts.view
def home(request):
  if not request.user.is_authenticated: 
    return redirect('login')
  
  if request.user.is_staff:
    return redirect('welcome')

  #for now query all posts: this will eventually be followed scoped
  posts = Post.objects.order_by('-id').all()

  return render(request, 'home.html', {
    'posts': posts
  })

#Posts.create
def createPost(request):
  return render(request, 'posts/create_post.html', {})

#Posts.store
def storePost(request):
  if not request.user.is_authenticated: 
    return redirect('login')

  user = request.user
  profile = Profile.objects.filter(user_id = user.id).first()
  title = request.GET['title']
  body = request.GET['description']
  rec_song_id = request.GET['rec_song_id']
  rec_album_id = request.GET['rec_album_id']

  if title == None or  title == '':
    messages.error(request, 'A title is REQUIRED')
    return render(request, 'posts/create_post.html', {})
  
  if len(body) > 240:
    messages.error(request, 'Your description was too long')
    return render(request, 'posts/create_post.html', {})

  post = Post.objects.create(
    user_id = user,
    profile = profile,
    title = title,
    description = body,
    rec_song_id = rec_song_id,
    rec_album_id = rec_album_id
  )
  post.save()

  return redirect('home')

def editPost(request, post_id):
  if not request.user.is_authenticated: 
    return redirect('login')

  if request.user.is_staff:
    return redirect('welcome')
  
  post = Post.objects.filter(id = post_id).first()

  if post is None:
    return redirect('welcome')

  if request.user != post.user_id:
    return redirect('welcome')
  
  title = request.GET['title']
  description = request.GET['description']

  if title == '':
    title = post.title
  
  if description == '':
    description = post.description
  
  post.title = title
  post.description = description
  post.save()

  messages.success(request, 'Your post has been updated!')
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def deletePost(request, post_id):
  if not request.user.is_authenticated: 
    return redirect('login')

  if request.user.is_staff:
    return redirect('welcome')
  
  post = Post.objects.filter(id = post_id).first()

  if post is None:
    return redirect('welcome')

  if request.user != post.user_id:
    return redirect('welcome')
  
  post.delete()

  messages.success(request, 'Your post is deleted!')
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  

#Like post
def likePost(request, pk):
  user = request.user
  post = Post.objects.filter(id=pk)[0]
  if Like.objects.filter(user_id = user, post_id = post).first() == None:
    like = Like.objects.create(
      user_id = user,
      post_id = post,
      like_type = 'Like'
    )
    like.save()
  return HttpResponseRedirect(request.POST.get('next', '/'))

#Unlike post
def unlikePost(request, pk):
  post = Post.objects.filter(id=pk)[0]
  like = Like.objects.filter(user_id = request.user, post_id = post).first()
  if like != None:
    like.delete()
  return HttpResponseRedirect(request.POST.get('next', '/'))


