from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = routers.SimpleRouter()
router.register(r'api/bank-customers', views.BankCustomerViewSet)
router.register(r'api/bank-accounts', views.BankAccountViewSet)
router.register(r'api/bank-transfers', views.BankTransferViewSet)

urlpatterns = [

    path('login', views.login_view, name='login_view'),
    path('logout', views.logout_view, name='logout_view'),
    path('sinup', views.signup, name='signup'),
    path('home', views.loadhome, name='loadhome'),
    path('create-transfer', views.create_transfer, name='create-transfer'),
    path('logout', views.logout_view, name='logout'),
    path('test', views.test, name='test'),
    path('nolog', views.login_failed, name='login_failed'),
    path('create-transfer-v2', views.CreateTransferView.as_view(), name='create-transfer-v2'),
    path('', views.index, name='bank_index'),
]
urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)
