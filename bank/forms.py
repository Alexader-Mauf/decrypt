import bleach
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field, ButtonHolder
from django import forms
from django.contrib.auth.models import User

from core import models


class CreateTransferForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.accounts_from = kwargs.pop('accounts_from')
        super(CreateTransferForm, self).__init__(*args, **kwargs)
        self.fields["verwendungszweck"] = forms.CharField(
            label="Verwendungszweck",
            required=True
        )
        self.fields["amount"] = forms.DecimalField(
            label="Überweisungsbetrag",
            required=True,
            min_value=0.01
        )
        self.fields["iban_to"] = forms.CharField(
            label="Empfänger",
            required=True
        )
        self.fields["iban_from"] = forms.ChoiceField(
            label="Abbsender",
            required=True,
            choices=[(x.iban, "{} {}".format(x.name, x.iban)) for x in self.accounts_from],
        )
        self.fields["instant_transfer"] = forms.BooleanField(
            label="Sofortüberweisung",
            required=False
        )
        self.helper = FormHelper()

        self.helper.add_input(Submit('submit', 'absenden'))

        self.helper.layout = Layout(

            Div(
                Div(
                    Field('iban_from', css_class="form-control"),
                    css_class="col-sm-12"
                ),
                Div(
                    Field('iban_to', "Empfänger", css_class="form-control"),
                    css_class="col-sm-12"
                ),
                Div(
                    Field('amount', "Überweisungsbetrag", css_class="form-control"),
                    css_class="col-12"
                ),
                Div(
                    Field('verwendungszweck', "Verwendungszweck", css_class="form-control"),
                    css_class="col-12"
                ),
                Div(
                    Field('instant_transfer', "Sofortüberweisung"),
                    css_class="col-12"
                ),
                css_class="row g-3"

            )
        )

    def is_valid(self):
        is_valid = super(CreateTransferForm, self).is_valid()
        cd = self.clean()
        if not is_valid:
            return False
        if cd["verwendungszweck"].strip() == "":
            self.add_error("verwendungszweck", "Bitte Verwendungswzweck angeben")
            return False
        account_to = models.BankAccount.objects.filter(iban=cd["iban_to"]).first()
        if account_to is None:
            self.add_error("iban_to", "Konto mit IBAN existiert nicht")
            return False

        return True

    def clean_xss(self):
        data = self.cleaned_data
        data['verwendungszweck'] = bleach.clean(data.get('verwendungszweck', ''))

    def clean(self):
        cd = super(CreateTransferForm, self).clean()
        self.clean_xss()
        return cd



class LoginForm(forms.Form):
    username = forms.CharField(label='Nutzername', max_length=255)
    password = forms.CharField(widget=forms.PasswordInput(), label='Passwort', max_length=255)
    remember_user = forms.BooleanField(
        required=False,
        label='Remember Me'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('username', css_class='input-group mb-3'),
                    #css_class='col-xs-12',
                ),
                Div(
                    Field('password', css_class='input-sm'),
                    #css_class='col-xs-12',
                ),
                Div(
                    Field('remember_user', css_class="custom-control custom-checkbox")
                ),
                Div(
                    ButtonHolder(
                        Submit('submit', "Login", css_class='btn btn-primary btn-block'),
                    ),
                    #css_class='col-xs-12',
                ),

                #css_class="row"
            )
        )

    def is_valid(self):
        is_valid = super(LoginForm, self).is_valid()
        if not is_valid:
            return False
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except Exception as e:
            self.add_error("username", "Nutzer existiert nicht")
            return False

        if not user.check_password(self.cleaned_data['password']):
            self.add_error("password", "Passwort falsch")
            return False

        return True
