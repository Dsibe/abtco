from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'class': 'name-form'}))
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'last-name-form'}))

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password1',
            'password2'
        ]
