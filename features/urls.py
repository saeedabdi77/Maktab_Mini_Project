from django.urls import path, include
from .views import *

urlpatterns = [
    path('home/', Base.as_view(), name="home"),
]
