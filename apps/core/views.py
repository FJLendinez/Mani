from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import redirect, render


@login_required()
def index(request):
    return redirect('/transactions/')
    # return render(request, 'pages/index.html', {})


@login_required()
def send_test_email(request):
    subject, from_email, to = "hello", "from@example.com", "to@example.com"
    text_content = "This is an important message."
    html_content = "<p>This is an <strong>important</strong> message.</p>"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return HttpResponse("<strong>Mail sent</strong>")


@login_required()
def store_in_cache(request):
    value = cache.get('from-cache')
    if not value:
        cache.set('from-cache', "Yes", timeout=3)
        value = "No"
    return HttpResponse(value)
