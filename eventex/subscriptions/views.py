from django.core import mail
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import SubscriptionForm


def subscribe(request):
    if request.POST:
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            body = render_to_string("subscriptions/subscription_email.txt", form.cleaned_data)
            mail.send_mail(
                'Confirmação de inscrição',
                body,
                'contato@eventex.com.br',
                ['contato@eventex.com.br', form.cleaned_data['email']]
            )
            messages.success(request, 'Inscrição realizada com sucesso!')
            return HttpResponseRedirect(reverse("subscriptions:subscribe"))
        else:
            return render(request, "subscriptions/subscription_form.html", {'form': form})

    context = {
        'form': SubscriptionForm()
    }
    return render(request, "subscriptions/subscription_form.html", context)
