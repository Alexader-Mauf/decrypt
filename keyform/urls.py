from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from key import views as apiviews


urlpatterns = [
    path('index', views.index, name='formdex'),
    path('create-secretnote', views.create_secretnote, name='create_secretnote'),
    path('encode-decode', views.encode_decode, name='encode_decode'),
    path('home/<uuid>/', views.load_secretnote, name='load_secretnote'),
    path('decode', views.decode, name='decode'),
    path('apistyles', apiviews.index, name='apistyle'),
    #path('home?message=<uuid>', views.load_secretnote, name='load_secretnote'),
]
