from django.db import transaction
from django.shortcuts import render, redirect
from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from core import models
from . import serializers

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login

from rest_framework import status
from rest_framework.response import Response


def _generate_iban():
        import random
        output = "DE82"
        BLZ = random.randint(10000000,99999999)
        output+=BLZ
        Kontonummer=random.randint(10**10,9*10**10)
        output+=Kontonummer

def login(request):
    return render(request, "login.html")

def loadhome(request):
    return render(request, 'home2.html', {
        "statusmsg": "user existiert"

                  })

def index(request):
    # getting usernames as post from login
    usname = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=usname, password=password)
    if user is not None:

        return redirect('/bank/redirect')

    else:
        output = str(usname) + str(password)
        return render(request, "login.html", {
            "statusmsg": output
        })


def signup(request):
    return render(request, "signup.html")


def createuser(request):
    # get data from a form
    vorname = request.POST.get("vorname")
    nachname = request.POST.get("name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    passwordcheck = request.POST.get("passwordcheck")
    if password != passwordcheck:
        return render(request, "signup.html", {
            "statusmsg": "Passwörter stimmen nicht überein.",
        })
    else:
        user = User.objects.create_user(username, email, password, first_name=vorname, last_name=nachname)
        user.save()

        #
        from django.contrib.auth.models import Group
        group = Group.objects.get(name='Bankkunden')
        group.user_set.add(user)
        group.save()

        return render(request, "signup.html", {
            "statusmsg": "Nutzer erfolgreich erstellt./"
                         "vorname:{}/"
                         "nachname:{}/"
                         "email:{}/"
                         "password:{}".format(vorname, nachname, email, password),
        })


def update_adress(request, user_id):
    user = User.objects.get(pk=user_id)
    newadress = request.POST.get("adress")
    user.BankCustomer.adress = newadress
    user.save()


class BankCustomerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BankCustomersSerializer
    queryset = models.BankCustomer.objects.order_by('id')
    permission_classes = [IsAuthenticated]  # (IsAuthenticated, DjangoModelPermission)
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication)  # zur authorisierung und errfüllung des tests(SessionAuthentication, BasicAuthentication)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = {
        'vorname': ['exact'],
        'created_at': ['gte', 'lte'],
        'updated_at': ['gte', 'lte'],
        'name': ['exact'],
        'email': ['exact'],
    }


class BankAccountViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BankAccountSerializer
    queryset = models.BankCustomer.objects.order_by('id')
    permission_classes = [IsAuthenticated,] #DjangoModelPermission]
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication)  # zur authorisierung und errfüllung des tests(SessionAuthentication, BasicAuthentication)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = {
        'balance': ['exact'],
        'created_at': ['gte', 'lte'],
        'updated_at': ['gte', 'lte'],
        'iban': ['exact'],
        'inhaber': ['exact'],
        'name': ['exact'],
    }



class BankTransferViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BankTransferSerializer
    queryset = models.BankTransfer.objects.order_by('id')
    permission_classes = [IsAuthenticated]  # (IsAuthenticated, DjangoModelPermission)
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication)  # zur authorisierung und errfüllung des tests(SessionAuthentication, BasicAuthentication)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = {
        'amount': ['exact'],
        'created_at': ['gte', 'lte'],
        'updated_at': ['gte', 'lte'],
        'iban_from': ['exact'],
        'iban_to': ['exact'],
    }

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            if request.user.bank_accounts.filter(iban=serializer.valid_data.get("iban_from")).first() is not None:
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)