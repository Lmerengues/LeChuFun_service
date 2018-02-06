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

    contact_dis = {}


    openid = request.GET['openid']








    cursor = connections['klook'].cursor()
    cursor.execute("select uname,uphone,uemail from contact where uno = %s order by utime desc", (openid,))
    contact_dis = dictfetchall(cursor)
    cursor.close()

    hiscontact = {}
    if len(contact_dis) >0:
        hiscontact = contact_dis[0]

    dict = hiscontact

    cursor = connections['klook'].cursor()
    cursor.execute("select * from activity_package where pno = %s", (request.GET['pno'],))
    dict['package'] = dictfetchall(cursor)[0]
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select atitle1 from activities where ano = %s", (dict['package']['ano'],))
    dict['atitle'] = dictfetchall(cursor)[0]['atitle1']
    cursor.close()

    response = HttpResponse(json.dumps(dict),content_type="application/json")
    return response

def submit(request):

    openid = request.GET['openid']
    name = request.GET['uname']
    email = request.GET['uemail']
    phone = request.GET['uphone']

    #firm = request.GET['firm']
    #if firm == "undefined":
    #    firm = ""

    #dep = request.GET['dep']
    #if dep == "undefined":
    #   dep = ""

    #code = request.GET['code']
    #if code == "undefined":
    #    code = ""

    cursor = connections['klook'].cursor()
    cursor.execute("select cno from contact where uno = %s and uname = %s and uemail= %s and uphone = %s " ,(openid,name,email,phone,))
    contact_raw = dictfetchall(cursor)

    #response = HttpResponse(json.dumps(contact_raw), content_type="application/json")
    #return response


    cursor.close()
    if len(contact_raw) == 0:
        cursor = connections['klook'].cursor()
        cursor.execute("insert into contact values(null,%s,%s,%s,%s,sysdate())",
                       (openid,name,phone,email,))
        cursor.close()
        cursor = connections['klook'].cursor()
        cursor.execute("select cno from contact where uno = %s and uname = %s "
                       "and uemail= %s and uphone = %s ", (openid, name, email, phone,))
        cno_raw = dictfetchall(cursor)
        if len(cno_raw) == 1:
            cno = cno_raw[0]['cno']
    else:
        cno = contact_raw[0]['cno']

    response = HttpResponse(json.dumps({'cno':cno}), content_type="application/json")
    return response