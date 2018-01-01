from django.core.mail import send_mail

from django.http import HttpResponse

import json
from django.db import connections

import math

def index(request):
    send_mail('Subject here', 'Here is the message.', 'lechufun@163.com',
          ['317958662@qq.com'], fail_silently=False)