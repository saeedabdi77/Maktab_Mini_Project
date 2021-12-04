from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views import View
from .models import Post, Comment, Category, Tag
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DeleteCategoryForm, EditCategoryForm
from .forms import DeleteTagForm, EditTagForm
from django.urls import reverse
from django.db.models import Count


def home(request):
    posts = Post.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'home.html', {'posts': posts, 'categories': categories})


class CategoryList(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'categories'


def category_detail(request, title):
    category = Category.objects.get(title=title)
    posts = category.post_set.all()
    return render(request, 'category-detail.html', {'category': category, 'posts': posts})


def edit_category(request, title):
    category = get_object_or_404(Category, title=title)
    form = EditCategoryForm(instance=category)

    if request.method == "POST":
        form = EditCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect(reverse('category'))

    return render(request, 'edit-category.html', {'form': form, 'category': category})


def delete_category(request, title):
    category = get_object_or_404(Category, title=title)

    form = DeleteCategoryForm(instance=category)
    if request.method == "POST":
        category.delete()
        return redirect(reverse('category'))

    return render(request, 'delete-category.html', {'form': form, 'category': category})


class AddCategory(View):
    form = EditCategoryForm

    def get(self, request, *args, **kwargs):
        return render(request, 'add-category.html', {'form': self.form})

    def post(self, request, *args, **kwargs):
        post_form = self.form(request.POST)
        if post_form.is_valid():
            post_form.save()
            return redirect(reverse('category'))


class TagList(ListView):
    model = Tag
    queryset = Tag.objects.annotate(posts=Count('post'))
    template_name = 'tags.html'
    context_object_name = 'tags'


def tag_detail(request, name):
    tag = Tag.objects.get(name=name)
    posts = tag.post_set.all()
    return render(request, 'tag-detail.html', {'tag': tag, 'posts': posts})


def edit_tag(request, name):
    tag = get_object_or_404(Tag, name=name)
    form = EditTagForm(instance=tag)

    if request.method == "POST":
        form = EditTagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect(reverse('tags'))

    return render(request, 'edit-tag.html', {'form': form, 'tag': tag})


def delete_tag(request, name):
    tag = get_object_or_404(Tag, name=name)

    form = DeleteTagForm(instance=tag)
    if request.method == "POST":
        tag.delete()
        return redirect(reverse('tags'))

    return render(request, 'delete-tag.html', {'form': form, 'tag': tag})


class AddTag(View):
    form = EditTagForm

    def get(self, request, *args, **kwargs):
        return render(request, 'add-tag.html', {'form': self.form})

    def post(self, request, *args, **kwargs):
        post_form = self.form(request.POST)
        if post_form.is_valid():
            post_form.save()
            return redirect(reverse('tags'))
