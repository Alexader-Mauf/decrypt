from django.db import transaction
from django.shortcuts import render
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from core import models
from . import serializers

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from django.auth import User
from django.contrib.auth import  authenticate

def login(request):
    return render(request, "login.html")


def index(request):
    # getting usernames as post from login
    username = "" #request.POST.get("username")
    password = "" #request.POST.get("password")


    user = authenticate(username=username, password=password)
    if user is not None:
        return render(request, "homescreen.html")
    else:
        return rrender(request, "login.html",{
            "statusmsg":"ungültige Zugangsdaten",
        })


def createuser(request):
    # get data from a form
    vorname = ""
    nachname = ""
    email = ""
    password = ""
    passwordcheck = ""
    if password != passwordcheck:
        return render(request, "signup.html",{
            "statusmsg" : "Passwörter stimmen nicht überein.",
        })
    user  = User.objects.create_user(vorname,email,password)
    user.last_name = nachname
    user.save()
    return render(request, "signup.html", {
        "statusmsg": "Nutzer erfolgreich erstellt.",
    })










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

