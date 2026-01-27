from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameAuthenticationForm(forms.Form):
    """
    Custom form to allow login via username or email.
    """
    login = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Username or Email"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_cache = None

    def clean(self):
        login_input = self.cleaned_data.get("login")
        password = self.cleaned_data.get("password")

        if login_input and password:
            # Try to get user by username
            user = authenticate(username=login_input, password=password)
            if not user:
                # Try to get user by email
                try:
                    user_obj = User.objects.get(email__iexact=login_input)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None

            if not user:
                raise forms.ValidationError("Invalid username/email or password")
            elif not user.is_active:
                raise forms.ValidationError("This account is inactive.")
            self.user_cache = user

        return self.cleaned_data

    def get_user(self):
        return self.user_cache
