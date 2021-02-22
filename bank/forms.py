import bleach
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms


class CreateTransferForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(CreateTransferForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'absenden'))

    verwendungszweck = forms.CharField(
        label="Verwendungszweck",
        widget=forms.Textarea(),
        required=True
    )

    amount = forms.DecimalField(
        label="Überweisungsbbetrag",
        widget=forms.Textarea(),
        required=True
    )

    iban_to = forms.CharField(
        label="Empfänger",
        widget=forms.Textarea(),
        required=True
    )

    iban_from = forms.CharField(
        label="Abbsender",
        widget=forms.Textarea(),
        required=True
    )

    def clean(self):
        cd = super().clean()
        self.clean_xss()
        return cd

    def is_valid(self):
        cd = self.clean()
        is_valid = super(CreateTransferForm, self).is_valid()
        if not is_valid:
            return False
        if cd["Verwendungszweck"] == " ":
            return False

    def clean_xss(self):
        data = self.cleaned_data
        data['text'] = bleach.clean(data['text'])
        return data
