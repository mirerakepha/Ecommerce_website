from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import password_validators_help_text_html

from .models import Profile

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import password_validators_help_text_html

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Customizing widgets with Bootstrap classes + placeholders
        self.fields['username'].widget.attrs.update({
            "placeholder": "Username",
            "class": "form-control"
        })
        self.fields['email'].widget.attrs.update({
            "placeholder": "Email",
            "class": "form-control"
        })
        self.fields['password1'].widget.attrs.update({
            "placeholder": "Password",
            "class": "form-control"
        })
        self.fields['password2'].widget.attrs.update({
            "placeholder": "Confirm Password",
            "class": "form-control"
        })

        # Add Django’s built-in password help text
        self.fields['password1'].help_text = password_validators_help_text_html()
        self.fields['password2'].help_text = "Enter the same password as before for verification."

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user



class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({"placeholder":"username", "class": "input-field"})
        self.fields['password'].widget.attrs.update({"placeholder":"password", "class": "input-field"})



class UpdateUserForm(UserChangeForm):
    password = None  # hide password field

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "Email",
            "class": "form-control"
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "First Name",
            "class": "form-control"
        })
    )
    last_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Last Name",
            "class": "form-control"
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            "placeholder": "Username",
            "class": "form-control"
        })


class ChangePasswordForm(SetPasswordForm):
    class meta:
        model = User
        fields = ['new_password1', 'new_password2']





class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_pic", "location", "address", "country"]
        widgets = {
            'location': forms.TextInput(attrs={'id': 'location', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'id': 'address'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]