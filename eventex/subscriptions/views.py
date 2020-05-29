from django.conf import settings
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import SubscriptionForm
from .models import Subscription


def subscribe(request):
    if request.POST:
        return create(request)
    return new(request)


def create(request):
    form = SubscriptionForm(request.POST)
    if not form.is_valid():
        return render(request, "subscriptions/subscription_form.html", {'form': form})

    subscription = Subscription.objects.create(**form.cleaned_data)
    _send_mail(
        'Confirmação de inscrição',
        settings.DEFAULT_FROM_EMAIL,
        subscription.email,
        "subscriptions/subscription_email.txt",
        {'subscription': subscription}
    )

    return HttpResponseRedirect(reverse("subscriptions:thanks", kwargs={'id': subscription.id}))


def new(request):
    return render(request, "subscriptions/subscription_form.html", {'form': SubscriptionForm()})


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])


def thanks(request, id):
    subscription = get_object_or_404(Subscription, id=id)
    return render(request, "subscriptions/thanks.html", {'subscription': subscription})
