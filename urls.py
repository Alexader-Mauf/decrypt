from . import views
from django.urls import path

urlpatterns = [
    path('home', views.index, name='index'),
    path('create-secretnote', views.create_secretnote, name='create_secretnote'),
    path('secretnote/<uuid>/', views.load_secretnote, name='load_secretnote'),
    path('puredesign', views.testest, name='test_test'),
    path('decode', views.decode, name='decode'),
]
