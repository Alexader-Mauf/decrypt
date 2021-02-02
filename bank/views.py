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


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")
    if request.method == "POST":
        # getting usernames as post from login
        usname = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=usname, password=password)
        login(request, user)
        if user is not None:
            login(request, user)
            return redirect(reverse('loadhome'))
        else:
            output = f"Nutzername und Passwort nicht bekannt"
            return render(request, "login.html", {
                "statusmsg": output
            })


def logout_view(request):
    logout(request)
    return redirect(reverse('bank_index'))


def loadhome(request):

    bankaccounts = request.user.bank_customer.bankaccounts.all()

    print(bankaccounts)

    if request.user.is_authenticated:
        return render(request, 'home2.html', {
            "user": request.user,
            "accounts":bankaccounts
        })
    else:
        return redirect(reverse('bank_index'))


def index(request):
    return render(request, "login.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html")

    if request.method == "POST":
        #POST
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
            # user wird erstellt

            user = User.objects.create_user(username, email, password, first_name=vorname, last_name=nachname)
            user.save()
            user = User.objects.get(username=username)

            # user wird der folgenden rechtegruppe zugewiesen

            group = Group.objects.get(name='Bankkunden')
            group.user_set.add(user)
            group.save()

            customer = models.BankCustomer.objects.create(
                user=user,
                adress="",
            )
            customer.save()

            account = models.BankAccount.objects.create(
                name="geld",
                account_owned_by=customer
            )
            account.save()



            return render(request, "signup.html", {
                "statusmsg": """
                Nutzer erfolgreich erstellt
                vorname:{}
                nachname:{}
                email:{}
                password:{}
                """.format(vorname, nachname, email, password).strip(),
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
        #'name':['exact'],
        'adress' : ['exact'],
        'created_at': ['gte', 'lte'],
        'updated_at': ['gte', 'lte'],
    }

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return super(BankCustomerViewSet, self).get_queryset()
        else:
            return super(BankCustomerViewSet, self).get_queryset().filter(user=user)


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

