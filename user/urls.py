from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', login_account, name='login'),
    path('logout/', logout_account, name='logout'),
    path('signup/', signup, name='signup'),
]
