from django.urls import path, include
from .views import *

urlpatterns = [
    path('home/', home, name="home"),
    path('categories/', CategoryList.as_view(), name="category"),
    path('categories/<str:title>/', category_detail, name="category-detail"),
    path('categories/edit/<str:title>/', edit_category, name="edit-category"),
    path('categories/delete/<str:title>/', delete_category, name="delete-category"),
    path('add-category/', AddCategory.as_view(), name="add-category"),
    path('tags/', TagList.as_view(), name="tags"),
    path('tags/<str:name>/', tag_detail, name="tag-detail"),
    path('tags/edit/<str:name>/', edit_tag, name="edit-tag"),
    path('tags/delete/<str:name>/', delete_tag, name="delete-tag"),
    path('add-tag/', AddTag.as_view(), name="add-tag"),
]
