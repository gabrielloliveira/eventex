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
    return empty_form(request)


def empty_form(request):
    return render(request, "subscriptions/subscription_form.html", {'form': SubscriptionForm()})


def create(request):
    form = SubscriptionForm(request.POST)
    if not form.is_valid():
        return render(request, "subscriptions/subscription_form.html", {'form': form})

    subscription = form.save()
    _send_mail(
        'Confirmação de inscrição',
        settings.DEFAULT_FROM_EMAIL,
        subscription.email,
        "subscriptions/subscription_email.txt",
        {'subscription': subscription}
    )

    return HttpResponseRedirect(reverse("subscriptions:thanks", kwargs={'uuid': subscription.uuid}))


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])


def thanks(request, uuid):
    subscription = get_object_or_404(Subscription, uuid=uuid)
    return render(request, "subscriptions/thanks.html", {'subscription': subscription})
