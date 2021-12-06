from django import forms
from .models import Tag, Post, Category, Comment
from django.contrib.auth.models import User
from user.models import ExtendUser
from django.core.exceptions import ValidationError


class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']


class DeleteCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = []


class EditTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


class DeleteTagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = []


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['publisher', 'slug', 'likes']


class UpdatePublishedPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['publisher', 'slug', 'likes', 'status']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text']
