from django import forms
from .models import ShippingAddress


class ShippingForm(forms.ModelForm):
    shipping_fullname = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'FullName'}), required=False)
    shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), required=False)
    shipping_street = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}), required=False)
    shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}), required=False)
    shipping_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}), required=False)
    shipping_zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZipCode'}), required=False)
    shipping_country = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}), required=False)
    shipping_phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}), required=False)

    class Meta:
        model = ShippingAddress
        fields = ['shipping_fullname', 'shipping_email', 'shipping_street', 'shipping_city', 'shipping_state', 'shipping_zipcode', 'shipping_country', 'shipping_phone']
        exclude = ['user', ]


