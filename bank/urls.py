from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.SimpleRouter()
router.register(r'api/bank_customers', views.BankCustomerViewSet)
router.register(r'api/bank_accounts', views.BankAccountViewSet)
urlpatterns = [
    path('home', views.index, name='index'),
    path('login', views.login, name='login'),
    path('sinup', views.signup, name='signup'),
    path('', views.createuser, name='createuser'),
]

urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)