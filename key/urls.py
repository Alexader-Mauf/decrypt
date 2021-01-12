from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.SimpleRouter()
router.register(r'api/secret-msgs', views.SecretMsgViewSet)
urlpatterns = [
    path('home', views.index, name='index'),
    path('create-secretnote', views.create_secretnote, name='create_secretnote'),
    path('encode-decode', views.encode_decode, name='encode_decode'),
    path('secretnote/<uuid>/', views.load_secretnote, name='load_secretnote'),
    path('decode', views.decode, name='decode'),
]

urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)

