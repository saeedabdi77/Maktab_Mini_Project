from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ExtendUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, min_length=5)
    password = forms.CharField(widget=forms.PasswordInput)


GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )


class SignUpForm(UserCreationForm):
    gender = forms.ChoiceField(
        required=True,
        choices=GENDER_CHOICES,
    )
    image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'image', 'gender', 'password1', 'password2')
