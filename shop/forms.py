from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *


class UserUpdateForm(ModelForm):
    new_username = forms.CharField(required=True, initial='username')
    first_name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={'class': 'name-form'}))
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'last-name-form'}))

    def clean(self):
        cleaned_data = super(UserUpdateForm, self).clean()
        new_username = cleaned_data['new_username']
        
        if User.objects.filter(username=new_username).exists():
            if request.user.username != new_username:
                raise forms.ValidationError('This username already exists.')
        
        return cleaned_data

    class Meta:
        model = User
        fields = ['new_username', 'first_name', 'last_name']


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
