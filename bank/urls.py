from django.urls import path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

router = routers.SimpleRouter()
router.register(r'api/bank_customers', views.BankCustomerViewSet)
urlpatterns = [
    path('home', views.index, name='index'),
]

urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)