from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.SimpleRouter()
router.register(r'api/bank-customers', views.BankCustomerViewSet)
router.register(r'api/bank-accounts', views.BankAccountViewSet)
router.register(r'api/bank-transfers', views.BankTransferViewSet)


urlpatterns = [
    path('', views.make_transfers, name='make_transfers')
]
urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)