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
from datetime import date, datetime,time as time2
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


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date, time2)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))
def dictfetchall(cursor):
	desc = cursor.description
	return [
	dict(zip([col[0] for col in desc], row))
    	for row in cursor.fetchall()
    	]

def index(request):

    oid = '1514813084'
    tcursor = connections['default'].cursor()
    tcursor.execute("select orders.oid,orders.hno,odate,ostart,oend,otype,onum,oready,obarbecue,"
                    "ofapiao,otip,ototal,orders.ocno,otime,htitle1,htitle2,uname,uphone,uwechat,ufirm,udepartment from orders,contact,house "
                    "where oid = %s and orders.ono = contact.cno and orders.hno = house.hno", (oid,))
    raw = dictfetchall(tcursor)
    tcursor.close()

    my_type = ['聚会派对', '团建年会']
    my_num = ['1-5', '6-10', '11-20', '21-30']
    my_is = ['是', '否']

    str1 = '<p>订单号:' + raw[0]['oid'] + '</p>'
    str1 += '<p>场地名:' + raw[0]['htitle1'] + "·" + raw[0]['htitle2'] + '</p>'
    str1 += '<p>预约者姓名:' + raw[0]['uname'] + '</p>'
    str1 += '<p>预约者微信:' + raw[0]['uwechat'] + '</p>'
    str1 += '<p>预约者电话:' + raw[0]['uphone'] + '</p>'
    str1 += '<p>预约者公司/部门:' + raw[0]['ufirm'] + "/" + raw[0]['udepartment'] + '</p>'
    str1 += '<p>预约时间:' + json_serial(raw[0]['odate']) + "   " + json_serial(raw[0]['ostart']) + "-" + json_serial(
        raw[0]['oend']) + '</p>'
    str1 += '<p>下单金额:' + str(int(raw[0]['ototal']) / 100) + '</p>'
    str1 += '<p>下单时间:' + json_serial(raw[0]['otime']) + '</p>'
    str1 += '<p>预约类型:' + my_type[int(raw[0]['otype'])] + '</p>'
    str1 += '<p>预约人数:' + my_num[int(raw[0]['onum'])] + '</p>'
    str1 += '<p>是否需要准备:' + my_is[int(raw[0]['oready'])] + '</p>'
    str1 += '<p>是否需要烧烤设备:' + my_is[int(raw[0]['obarbecue'])] + '</p>'
    str1 += '<p>是否需要发票:' + my_is[int(raw[0]['ofapiao'])] + '</p>'
    str1 += '<p>附言:' + raw[0]['otip'] + '</p>'

    from_email = settings.DEFAULT_FROM_EMAIL

    msg = EmailMultiAlternatives('乐处Fun订单信息', str1, from_email,
                                 ['lechufun@163.com', 'liruishenshui@126.com'])

    msg.content_subtype = "html"
    msg.send()

    response = HttpResponse("test mail", content_type="application/json")
    return response