from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views import View
from .models import Post, Comment, Category, Tag, Like, DisLike
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DeleteCategoryForm, EditCategoryForm, CreatePostForm, UpdatePublishedPostForm
from .forms import DeleteTagForm, EditTagForm, CommentForm
from django.urls import reverse
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.paginator import Paginator


class Home(ListView):
    model = Post
    queryset = Post.objects.all().order_by('-created_at')
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'home.html'


class CategoryList(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'categories'


def category_detail(request, title):
    category = Category.objects.get(title=title)
    posts = category.post_set.all().order_by('-created_at')
    return render(request, 'category-detail.html', {'category': category, 'posts': posts})


@login_required(login_url='/myblog/login')
def edit_category(request, title):
    category = get_object_or_404(Category, title=title)
    form = EditCategoryForm(instance=category)

    if request.method == "POST":
        form = EditCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category edited!')
            return redirect(reverse('category'))

    return render(request, 'edit-category.html', {'form': form, 'category': category})


@login_required(login_url='/myblog/login')
def delete_category(request, title):
    category = get_object_or_404(Category, title=title)

    form = DeleteCategoryForm(instance=category)
    if request.method == "POST":
        category.delete()
        messages.warning(request, 'Category deleted!')
        return redirect(reverse('category'))

    return render(request, 'delete-category.html', {'form': form, 'category': category})


class AddCategory(LoginRequiredMixin, View):
    login_url = '/myblog/login/'
    form = EditCategoryForm

    def get(self, request, *args, **kwargs):
        return render(request, 'add-category.html', {'form': self.form})

    def post(self, request, *args, **kwargs):
        post_form = self.form(request.POST)
        if post_form.is_valid():
            post_form.save()
            messages.success(request, 'Category added!')
            return redirect(reverse('category'))
        else:
            messages.error(request, 'Category already exists!')
        return render(request, 'add-category.html', {'form': self.form})


class TagList(ListView):
    model = Tag
    queryset = Tag.objects.annotate(posts=Count('post'))
    template_name = 'tags.html'
    context_object_name = 'tags'


def tag_detail(request, name):
    tag = Tag.objects.get(name=name)
    posts = tag.post_set.all().order_by('-created_at')
    return render(request, 'tag-detail.html', {'tag': tag, 'posts': posts})


@login_required(login_url='/myblog/login')
def edit_tag(request, name):
    tag = get_object_or_404(Tag, name=name)
    form = EditTagForm(instance=tag)

    if request.method == "POST":
        form = EditTagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag edited!')
            return redirect(reverse('tags'))

    return render(request, 'edit-tag.html', {'form': form, 'tag': tag})


@login_required(login_url='/myblog/login')
def delete_tag(request, name):
    tag = get_object_or_404(Tag, name=name)

    form = DeleteTagForm(instance=tag)
    if request.method == "POST":
        tag.delete()
        messages.warning(request, 'Tag deleted!')
        return redirect(reverse('tags'))

    return render(request, 'delete-tag.html', {'form': form, 'tag': tag})


class AddTag(LoginRequiredMixin, View):
    login_url = '/myblog/login/'
    form = EditTagForm

    def get(self, request, *args, **kwargs):
        return render(request, 'add-tag.html', {'form': self.form})

    def post(self, request, *args, **kwargs):
        post_form = self.form(request.POST)

        if post_form.is_valid():
            post_form.save()
            messages.success(request, 'Tag added!')
            return redirect(reverse('tags'))
        else:
            messages.error(request, 'Tag already exists!')
        return render(request, 'add-tag.html', {'form': self.form})


class CreatePost(LoginRequiredMixin, View):
    login_url = '/myblog/login/'
    form = CreatePostForm

    def get(self, request, *args, **kwargs):
        return render(request, 'create-post.html', {'form': self.form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            form.instance.publisher = request.user.extenduser
            post = form
            post.save()
            return redirect(reverse('my-posts'))
        return render(request, 'create-post.html', {'form': self.form})


class MyPosts(LoginRequiredMixin, View):
    login_url = '/myblog/login/'
    template_name = 'my-posts.html'

    def get(self, request):
        queryset = Post.objects.filter(publisher=request.user.extenduser).order_by('-created_at')
        return render(request, self.template_name, {'posts': queryset})


@login_required(login_url='/myblog/login')
def edit_draft_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CreatePostForm(instance=post)

    if request.method == "POST":
        form = CreatePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('my-posts'))

    return render(request, 'create-post.html', {'form': form, 'post': post})


@login_required(login_url='/myblog/login')
def edit_published_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = UpdatePublishedPostForm(instance=post)

    if request.method == "POST":
        form = UpdatePublishedPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('my-posts'))

    return render(request, 'create-post.html', {'form': form, 'post': post})


@login_required(login_url='/myblog/login')
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    form = DeleteTagForm(instance=post)
    if request.method == "POST":
        post.delete()
        return redirect(reverse('my-posts'))

    return render(request, 'delete-post.html', {'form': form, 'post': post})


class SearchPageView(ListView):
    template_name = "search.html"
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = Post.objects.all()
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(title__contains=q) | Q(caption__contains=q))
        return queryset


class PostDetail(View):
    form = CommentForm

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        comments = post.comment_set.all()
        likes = post.like_set.all()
        dislikes = post.dislike_set.all()
        if request.user.is_authenticated:
            is_liked = False
            if likes.filter(user=request.user.extenduser).exists():
                is_liked = True
            is_disliked = False
            if dislikes.filter(user=request.user.extenduser).exists():
                is_disliked = True
            return render(request, 'post-detail.html',
                          {'post': post, 'comments': comments, 'form': self.form, 'likes': len(likes),
                           'dislikes': len(dislikes), 'is_liked': is_liked, 'is_disliked': is_disliked})
        else:
            return render(request, 'post-detail.html',
                          {'post': post, 'comments': comments, 'form': self.form, 'likes': len(likes),
                           'dislikes': len(dislikes)})

    @method_decorator(login_required(login_url='/myblog/login'))
    def post(self, request, slug):
        form = self.form(request.POST)
        if form.is_valid():
            if request.POST.get('parent_id'):
                form.instance.parent = Comment.objects.get(id=int(request.POST.get('parent_id')))
            form.instance.publisher = request.user.extenduser
            form.instance.post = Post.objects.get(slug=slug)
            comment = form
            comment.save()

        post = Post.objects.get(slug=slug)
        comments = post.comment_set.all()
        likes = post.like_set.all()
        dislikes = post.dislike_set.all()
        if request.POST.get('liked_id'):
            if likes.filter(user=request.user.extenduser).exists():
                Like.objects.get(post=post, user=request.user.extenduser).delete()
            else:
                Like.objects.create(post=post, user=request.user.extenduser)
        if request.POST.get('disliked_id'):
            if dislikes.filter(user=request.user.extenduser).exists():
                DisLike.objects.get(post=post, user=request.user.extenduser).delete()
            else:
                DisLike.objects.create(post=post, user=request.user.extenduser)

        is_liked = False
        if likes.filter(user=request.user.extenduser).exists():
            is_liked = True
        is_disliked = False
        if dislikes.filter(user=request.user.extenduser).exists():
            is_disliked = True
        return render(request, 'post-detail.html',
                      {'post': post, 'comments': comments, 'form': self.form, 'likes': len(likes),
                       'dislikes': len(dislikes), 'is_liked': is_liked, 'is_disliked': is_disliked})
