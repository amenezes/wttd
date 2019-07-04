from django.core import mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, Http404
from django.conf import settings
from django.shortcuts import resolve_url as r

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription

from itsdangerous import URLSafeSerializer


def new(request):
    if request.method == 'POST':
        return create(request)

    return empty_form(request)


def empty_form(request):
    return render(
        request,
        'subscriptions/subscription_form.html',
        {"form": SubscriptionForm()})


def create(request):
    form = SubscriptionForm(request.POST)

    if not form.is_valid():
        return render(
            request, 'subscriptions/subscription_form.html',
            {'form': form})

    subscription = Subscription.objects.create(**form.cleaned_data)

    _send_mail(
        'Confirmação de inscrição',
        settings.DEFAULT_FROM_EMAIL,
        subscription.email,
        'subscriptions/subscription_email.txt',
        {'subscription': subscription})    
    subscription_id = encode_subscription_id(subscription.pk)

    return HttpResponseRedirect(r('subscriptions:detail', subscription_id))


def encode_subscription_id(identifier):
    property_serializer = URLSafeSerializer(settings.SECRET_KEY)
    return property_serializer.dumps(identifier)


def decode_subscription_id(identifier):
    property_serializer = URLSafeSerializer(settings.SECRET_KEY)
    return property_serializer.loads(identifier)


def detail(request, pk):
    try:
        subscription_id = decode_subscription_id(pk)
        subscription = Subscription.objects.get(pk=subscription_id)
    except Subscription.DoesNotExist:
        raise Http404

    return render(
        request,
        'subscriptions/subscription_detail.html',
        {'subscription': subscription}
    )


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, from_, [from_, to])
