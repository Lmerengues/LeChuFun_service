#!/usr/bin/python
#coding:utf-8
from django.http import HttpResponse
import urllib
import json
import hashlib
from django.db import connections
import logging
import random
import string
#import datetime
from datetime import date, datetime, time as time2
import time
import urllib2
import requests
#cursor = connections['default'].cursor()
import xml.etree.ElementTree as ET
#from flask import Flask, request, jsonify
#from datetime import date, datetime
import pytz
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def index(request):
    url = "https://api.weixin.qq.com/cgi-bin/token"
    querystring = {"grant_type": "client_credential", "appid": "wx08912a543bda29bc",
                   "secret": "0b0d2c8666c0504d696c5cddd342ba17"}
    headers = {}
    response = requests.request("GET", url, headers=headers, params=querystring)
    access_token = json.loads(response.text)['access_token']

    url = "https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token=ACCESS_TOKEN="+access_token

    tmpdata={"scene":'5',"page":"pages/detail/detail"}
    req = urllib2.Request(url, json.dumps(tmpdata), headers={'Content-Type': 'application/json'})
    result = urllib2.urlopen(req, timeout=30).read()

    resp = HttpResponse(json.dumps(result), content_type="application/json")
    return resp
