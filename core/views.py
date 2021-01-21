from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from core import models
from . import serializers
# Create your views here.





def make_transfers(request):
    return redirect('index')


class BankCustomerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BankCustomersSerializer
    queryset = models.BankCustomer.objects.order_by('id').all()
    permission_classes = [IsAuthenticated]  # (IsAuthenticated, DjangoModelPermission)
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication)  # zur authorisierung und errfüllung des tests(SessionAuthentication, BasicAuthentication)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = {
        #'name':['exact'],
        'adress' : ['exact'],
        'created_at': ['gte', 'lte'],
        'updated_at': ['gte', 'lte'],
    }


class BankTransferViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BankTransferSerializer
    queryset = models.BankTransfer.objects.all()
    permission_classes = [IsAuthenticated]  # (IsAuthenticated, DjangoModelPermission)
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication)  # zur authorisierung und errfüllung des tests(SessionAuthentication, BasicAuthentication)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)



class BankAccountViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BankAccountSerializer
    queryset = models.BankAccount.objects.all()
    permission_classes = [IsAuthenticated]  # (IsAuthenticated, DjangoModelPermission)
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication)  # zur authorisierung und errfüllung des tests(SessionAuthentication, BasicAuthentication)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
