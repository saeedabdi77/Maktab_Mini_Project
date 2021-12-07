from django.urls import path, include
from .views import *

urlpatterns = [
    path('contact-us/', get_message, name='get-message'),
    path('thanks-for-submission/', Submission.as_view()),
]