from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm, UpdateProfilePhotoForm, SetNewPasswordForm
from .models import ExtendUser
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


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
                next = request.GET.get('next')
                if next:
                    return redirect(request.GET.get('next'))
                return redirect(reverse('home'))
            else:
                message = 'Username or password is incorrect!'

    return render(request, 'login-form.html', {'form': form, 'message': message})


def logout_account(request):
    logout(request)
    return redirect(reverse('home'))


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
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


class ChangeProfilePhoto(LoginRequiredMixin, View):
    login_url = '/myblog/login/'
    template_name = 'change-profile.html'
    form = UpdateProfilePhotoForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            user = request.user.extenduser
            user.image = form.cleaned_data.get('image')
            user.save()
            return redirect(reverse('my-posts'))
        return render(request, self.template_name, {'form': self.form})


@login_required(login_url='/myblog/login')
def set_new_password(request):
    form = SetNewPasswordForm()
    if request.method == "POST":
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.check_password(form.cleaned_data.get('password')):
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect(reverse('my-posts'))

    return render(request, 'new-password.html', {'form': form})
