from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import *

# Create your views here.
def home(request):
  return render(request, 'home.html', {})