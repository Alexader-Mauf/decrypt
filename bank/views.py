from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from core import models
from . import serializers

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

def login(request):
    return render(request, "login.html")


def index(request):
    return render(request, "homescreen.html")








class BankCustomerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BankCustomersSerializer
    queryset = models.BankCustomer.objects.order_by('id')
    permission_classes = [IsAuthenticated]#(IsAuthenticated, DjangoModelPermission)
    authentication_classes = (SessionAuthentication, BasicAuthentication)# zur authorisierung und errfüllung des tests(SessionAuthentication, BasicAuthentication)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = {
        'vorname':['exact'],
        'created_at':['gte', 'lte'],
        'updated_at':['gte', 'lte'],
        'name':['exact'],
        'email':['exact'],
    }



class BankAccountViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BankAccountSerializer
    queryset = models.BankCustomer.objects.order_by('id')
    permission_classes = [IsAuthenticated]#(IsAuthenticated, DjangoModelPermission)
    authentication_classes = (SessionAuthentication, BasicAuthentication)# zur authorisierung und errfüllung des tests(SessionAuthentication, BasicAuthentication)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = {
        'balance':['exact'],
        'created_at':['gte', 'lte'],
        'updated_at':['gte', 'lte'],
        'IBAN':['exact'],
        'inhaber':['exact'],
    }

