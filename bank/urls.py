from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.SimpleRouter()
router.register(r'api/bank-customers', views.BankCustomerViewSet)
router.register(r'api/bank-accounts', views.BankAccountViewSet)
router.register(r'api/bank-transfers', views.BankTransferViewSet)

urlpatterns = [
    path('', views.index, name='bank_index'),
    path('login', views.login_view, name='login_view'),
    path('logout', views.logout_view, name='logout_view'),
    path('sinup', views.signup, name='signup'),
    path('creation', views.createuser, name='createuser'),
    path('home', views.loadhome, name='loadhome')
]
urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)