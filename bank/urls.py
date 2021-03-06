from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

router = routers.SimpleRouter()
router.register(r'api/bank-customers', views.BankCustomerViewSet)
router.register(r'api/bank-accounts', views.BankAccountViewSet)
router.register(r'api/bank-transfers', views.BankTransferViewSet)

urlpatterns = [

    path('login', views.LoginView.as_view(), name='login_view'),
    path('logout', views.logout_view, name='logout_view'),
    path('sinup', views.signup, name='signup'),
    path('home', views.index, name='loadhome'),
    path('create-transfer', views.CreateTransferView.as_view(), name='create-transfer'),
    path('logout', views.logout_view, name='logout'),
    path('nolog', views.login_failed, name='login_failed'),
    path('create-transfer', views.CreateTransferView.as_view(), name='create-transfer'),
    path('', views.index, name='bank_index'),
    path('login2', views.LoginView.as_view(), name='new-login')
]
urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)
