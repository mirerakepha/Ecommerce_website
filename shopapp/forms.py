from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import Profile

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"placeholder":"username", "class": "input-field"})
        self.fields['email'].widget.attrs.update({"placeholder":"email", "class": "input-field"})
        self.fields['password1'].widget.attrs.update({"placeholder":"password", "class": "input-field"})
        self.fields['password2'].widget.attrs.update({"placeholder":"confirm_password", "class": "input-field"})



class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"placeholder":"username", "class": "input-field"})
        self.fields['password'].widget.attrs.update({"placeholder":"password", "class": "input-field"})



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_pic", "location", "delivery_center", "country"]
        widgets = {
            'location': forms.TextInput(attrs={'id': 'location', 'class': 'form-control'}),
            'delivery_center': forms.TextInput(attrs={'id': 'delivery_center'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]