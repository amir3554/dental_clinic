from typing import Any, Mapping
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Patient

attrs = { 'class' : 'form-control'}

class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        label='The Email',
        widget=forms.EmailInput(attrs=attrs)    
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs=attrs)
    )


class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs=attrs)
    )

    first_name = forms.CharField(
        label='first name',
        widget=forms.TextInput(attrs=attrs)
    )

    last_name = forms.CharField(
        label='last name',
        widget=forms.TextInput(attrs=attrs)
    )

    email = forms.EmailField(
        label='email',
        widget=forms.EmailInput(attrs=attrs)    
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs=attrs)
    )

    password2 = forms.CharField(
        label='Confirm your Password',
        widget=forms.PasswordInput(attrs=attrs)
    )

    bio = forms.CharField(
        label='bio',
        required=False,
        widget=forms.Textarea(attrs=attrs)
    )

    class Meta:
       model = Patient
       fields = [
            'username', 'first_name', 'last_name', 'email', 
            'password1', 'password2', 'bio'
        ]

