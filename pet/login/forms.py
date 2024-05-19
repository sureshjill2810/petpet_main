from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    middle_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)
    street_number = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    zip = forms.CharField(max_length=10)
    state = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=15)
    sex = forms.ChoiceField(choices=UserProfile.SEX_CHOICES)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'middle_name', 'last_name', 'email', 'password1', 'password2')

class SignInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(max_length=200)
