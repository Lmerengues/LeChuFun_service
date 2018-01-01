from django.core.mail import send_mail

from django.http import HttpResponse

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

import json
from django.db import connections

import math

def index(request):

    '''
    send_mail('Subject here', 'Here is the message.', 'lechufun@163.com',
          ['lechufun@163.com','317958662@qq.com'], fail_silently=False)
    '''

    from_email = settings.DEFAULT_FROM_EMAIL

    msg = EmailMultiAlternatives('title', '<p>test</p><p>again</p>', from_email, ['lechufun@163.com'])

    msg.content_subtype = "html"
    msg.send()

    response = HttpResponse("test mail", content_type="application/json")
    return response