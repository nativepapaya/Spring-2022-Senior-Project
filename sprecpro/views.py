from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import *

def welcome(request):
  return render(request, 'welcome.html', {})

def home(request):
  if not request.user.is_authenticated: 
    return redirect('welcome')

  return render(request, 'home.html', {})