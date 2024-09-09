from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(
        label='Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ['username', 'password']
