from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views import View
from .models import Post, Comment, Category, Tag


def home(request):

    posts = Post.objects.all()
    categories = Category.objects.all()
    return render(request, 'home.html', {'posts': posts, 'categories': categories})
