from django.contrib import admin
from sprecpro.models import *
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Profile)
admin.site.register(Favorite)