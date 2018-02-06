# !/usr/bin/env python
# -*- coding:utf-8 -*-
from django.http import HttpResponse

import json
from django.db import connections
import datetime


def dictfetchall(cursor):
	desc = cursor.description
	return [
	dict(zip([col[0] for col in desc], row))
    	for row in cursor.fetchall()
    	]


def index(request):

    openid = request.GET['openid']
    cursor = connections['default'].cursor()
    cursor.execute("select uname,uphone,uwechat from contact where uno = %s order by utime desc", (openid,))
    contact_dis = dictfetchall(cursor)
    cursor.close()

    hiscontact = {}
    if len(contact_dis) >0:
        hiscontact = contact_dis[0]

    dict = {'contact':hiscontact}

    response = HttpResponse(json.dumps(dict),content_type="application/json")
    return response