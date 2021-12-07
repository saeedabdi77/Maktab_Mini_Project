from django.contrib import admin
from .models import Post, Comment, Category, Tag, Like, DisLike
# Register your models here.

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(DisLike)
