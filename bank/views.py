import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core import models
from . import serializers
from .forms import CreateTransferForm, LoginForm
from .models import BankUserAdministration



def logout_view(request):
    logout(request)
    return redirect(reverse('bank_index'))


def index(request):
    if request.user.is_authenticated:
        try:
            bankaccounts = request.user.bank_customer.account_owned_by.all()
        except Exception as e:
            logout(request)
            return render(request, 'login.html', {
                "statusmsg": "keine Konten zu diesem Benutzer gefunden",
            })

        # der transfers call ist fehlerhaft (?) -> er gibt eine liste mit transfer-ids wieder
        # das transfers hat keine representation -> wirft fehler beim übermitteln
        # transfers = request.user.bank_customer.created_by.order_by("-created_at")[:10]
        transfers = models.BankTransfer.objects.filter(
            # iban from muss in Bank AccountAdministration sein
            Q(iban_from__in=request.user.bank_customer.account_owned_by.all()) |
            Q(iban_to__in=request.user.bank_customer.account_owned_by.all())
        ).all().order_by("-created_at")[:5]
        # print(bankaccounts, request.user, transfers)
        # for transfer in transfers:
        # print(transfer)
        return render(request, 'bank-index.html', {
            "user": request.user,
            "accounts": bankaccounts,
            "transfers": transfers,
        })
    else:
        return redirect(reverse('login_view'))


def login_failed(request):
    return render(request, "login.html", {
        "statusmsg": "Username or Password unknown"
    })




def signup(request):
    if request.method == "GET":
        # prüfen ob schon eingeloggt
        if request.user.is_authenticated:
            return redirect(reverse('loadhome'))
        return render(request, "signup.html")

    if request.method == "POST":
        # POST
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

            # die Rechtezuweisung ist dopelt gemoppelt jedoch ist keine Bankkunden Group
            # programmatisch festgehalten diese wurde via Django-Admin interface erstellt
            # vermutlich kann ich den folgenden code in der admin.py datein an der richtigen
            # Stelle anbringen um die Gruppe auch bei Datenbankverlust erhalten zu lassen.
            codenames = [
                'view_banktransfer',
                'add_banktransfer',
                'view_bankaccount',
                'view_bankcustomer',
                'change_bankcustomer',
            ]
            permissions = Permission.objects.filter(codename__in=codenames).all()

            user.user_permissions.set(permissions)
            user.save()

            return redirect(reverse("login_view"))


def update_adress(request, user_id):
    user = User.objects.get(pk=user_id)
    newadress = request.POST.get("adress")
    user.BankCustomer.adress = newadress
    user.save()


class LoginView(FormView):
    form_class = LoginForm
    lang = 'de'

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        if request.user.is_authenticated:
            return redirect(reverse('loadhome'))
        return render(request, 'login.html', {'form': form, })

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            cd = form.cleaned_data
            username = cd.get("username")
            password = cd.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if not cd.get("remember_user"):
                    request.session.set_expiry(0)
            if request.user.is_authenticated:
                return redirect(reverse('loadhome'))
        return render(
            request,
            'login.html',
            {'form': form}
        )


class CreateTransferView(FormView):
    form_class = CreateTransferForm
    lang = 'de'

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        kwargs = self.get_form_kwargs()
        kwargs['accounts_from'] = BankUserAdministration(self.request.user).adminstrating_accounts
        return form_class(**kwargs)

    def get(self, request, *args, **kwargs):
        self.request = request
        errors = request.session.get("core.CreateTransferView.errors")
        errors = json.loads(errors) if errors is not None else {}
        request.session["core.CreateTransferView.errors"] = None
        form = self.get_form()
        if not request.user.is_authenticated:
            return redirect(reverse('login_view'))
        if errors is not None:
            errors = [",".join(v) for k, v in errors.items()]
            errors = "<br>".join(errors) if len(errors) > 0 else None
        return render(request, 'transfer.html',
                      {'accounts': BankUserAdministration(request.user).adminstrating_accounts, 'form': form,
                       'errors': errors})

    def post(self, request, *args, **kwargs):
        self.request = request
        form = self.get_form()
        print(form.is_valid())
        if form.is_valid():
            cd = form.cleaned_data
            iban_from = cd.get("iban_from")
            iban_to = cd.get("iban_to")
            amount = cd.get("amount")
            use_case = cd.get("verwendungszweck")
            is_instant_transfer = cd.get("instant_transfer")
            print(
                iban_from,
                iban_to,
                amount,
                use_case,
                is_instant_transfer,
            )
            iban_to = models.BankAccount.objects.filter(iban=iban_to).first()
            iban_from = models.BankAccount.objects.filter(iban=iban_from).first()
            created_by = request.user.bank_customer
            transfer = models.BankTransfer.objects.create(
                iban_to=iban_to,
                iban_from=iban_from,
                amount=amount,
                use_case=use_case,
                created_by=created_by
            )
            transfer.save()

            if is_instant_transfer:
                transfer.run_transfer()
            return redirect(reverse('loadhome'))
        else:
            return render(
                request,
                'transfer.html',
                {'accounts': BankUserAdministration(request.user).adminstrating_accounts,
                 'form': form}
            )


class BankCustomerViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BankCustomersSerializer
    queryset = models.BankCustomer.objects.order_by('id').all()
    permission_classes = [IsAuthenticated]  # (IsAuthenticated, DjangoModelPermission)
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication)  # zur authorisierung und errfüllung des tests(SessionAuthentication, BasicAuthentication)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = {
        # 'name':['exact'],
        'adress': ['exact'],
        'created_at': ['gte', 'lte'],
        'updated_at': ['gte', 'lte'],
    }

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

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

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return super(BankTransferViewSet, self).get_queryset()
        else:
            return super(BankTransferViewSet, self).get_queryset().filter(
                Q(iban_from=user.bank_customer.account_owned_by.first()) |
                Q(iban_to=user.bank_customer.account_owned_by.first())
            )

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class BankAccountViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BankAccountSerializer
    queryset = models.BankAccount.objects.all()
    permission_classes = [IsAuthenticated]  # (IsAuthenticated, DjangoModelPermission)
    authentication_classes = (SessionAuthentication,
                              BasicAuthentication)  # zur authorisierung und errfüllung des tests(SessionAuthentication, BasicAuthentication)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return super(BankAccountViewSet, self).get_queryset()
        else:
            return super(BankAccountViewSet, self).get_queryset().filter(
                account_owned_by=user.bank_customer)  # hier muss ein "or" hin

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
