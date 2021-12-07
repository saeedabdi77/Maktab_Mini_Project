from django.shortcuts import render, redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm, UpdateProfilePhotoForm, SetNewPasswordForm, ForgetPasswordForm
from .models import ExtendUser
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
import random
import string


def login_account(request):
    form = LoginForm()
    message = ''
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        print(form.is_valid())
        if form.is_valid():
            user = authenticate(request, username=username, password=password)
            print(user)
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
            if user.email:
                subject = f"{form.cleaned_data.get('username')} thank you for registering to our blog"
                message = 'Hope you enjoy our blog!'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email]
                send_mail(subject, message, email_from, recipient_list)
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


class ForgetPassword(View):
    form = ForgetPasswordForm
    template_name = 'forget-password.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form})

    @staticmethod
    def password_generator():
        return f'{random.choice(string.ascii_letters)}{random.randint(10000000, 99999999)}'

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if not User.objects.filter(email=email).exists():
                messages.error(request, 'email not found!')
                return render(request, self.template_name, {'form': self.form})
            password = self.password_generator()
            print(password)
            subject = "new password for my blog"
            message = password
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            print(user.username)
            print(user.check_password(password))
            messages.success(request, 'New password is sent to your email')
            return redirect(reverse('login'))
        return render(request, self.template_name, {'form': self.form})


class ShowUserProfile(View):
    template_name = 'user-profile.html'

    def get(self, request, username):
        print(username)
        user_profile = User.objects.get(username=username)
        posts = user_profile.extenduser.post_set.all()
        print(4989)
        return render(request, self.template_name, {'user_profile': user_profile, 'posts': posts})
