from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ContactForm
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings


# contact-us form function
def get_message(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            subject = f"Message from {form.cleaned_data.get('email')}"
            message = form.cleaned_data.get('message')
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['DjangoProject.blogg@gmail.com']
            send_mail(subject, message, email_from, recipient_list)
            return HttpResponseRedirect('/myblog/thanks-for-submission/')
    else:
        form = ContactForm()
    return render(request, 'contact-us.html', {'form': form})


# TemplateView class to render thanks for submission page
class Submission(TemplateView):
    template_name = 'thanks-for-submission.html'
