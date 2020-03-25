from django.conf.urls import url,include
from django.contrib import admin
from . import views

app_name = 'contests'
urlpatterns = [
	url(r'^$', views.home, name='home'),
]
