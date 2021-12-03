from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm
from .models import ExtendUser
from django.contrib.auth.models import User
from django.contrib import messages


def login_account(request):
    form = LoginForm()
    message = ''
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        if form.is_valid():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('home'))
            else:
                message = 'Username or password is incorrect!'

    return render(request, 'login-form.html', {'form': form, 'message': message})


def logout_account(request):
    logout(request)
    return redirect(reverse('home'))


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.extenduser.image = form.cleaned_data.get('image')
            user.extenduser.gender = form.cleaned_data.get('gender')
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
