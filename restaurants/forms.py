from django import forms
from .models import OrderEntry


class AddressForm(forms.Form):
    address = forms.CharField(
        max_length=100, label='ADRES', help_text='podaj adres...')

# modelForm - tworzymy formularz na podstaiwe modelu i nie musimy definiowac wszystkich pol, mozemy to sobie uproscic


class OrderEntryForm(forms.ModelForm):
    class Meta:
        fields = ['course', 'quantity']
        model = OrderEntry
