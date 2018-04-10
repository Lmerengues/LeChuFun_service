#!/usr/bin/python
# coding:utf-8
from django.http import HttpResponse
import urllib
import json
import hashlib
from django.db import connections
import logging
import random
import string
# import datetime
from datetime import date, datetime, time as time2
import time
import urllib2
import requests
# cursor = connections['default'].cursor()
import xml.etree.ElementTree as ET
# from flask import Flask, request, jsonify
# from datetime import date, datetime
import pytz
from django.conf import settings
from django.core.mail import EmailMultiAlternatives



def send_email():
    str1 = "你"
    str1 += str(time.time())
    str += "是"
    str1 += str(time.time())
    str1  += "猹"

    from_email = settings.DEFAULT_FROM_EMAIL

    msg = EmailMultiAlternatives('我好困', str1, from_email,
                                 ['lechufun@163.com', '576817410@qq.com'])

    msg.content_subtype = "html"
    msg.send()

def index(request):

    cnt = 1
    while(1):
        send_email()
        time.sleep(10)
        cnt+=1
        if(cnt>5):
            break

    resp = HttpResponse(json.dumps({'status': 'success'}), content_type="application/json")
    return resp