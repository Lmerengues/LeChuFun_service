from django.http import HttpResponse

import json
from django.db import connections

from datetime import date, datetime,time

import math
import os

from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.base import ContentFile


def add_activity(request):

    basic_url = 'https://mina.mapglory.com/static/images/canaan/5.jpeg'

    cursor = connections['klook'].cursor()
    #cursor.execute("insert into activities values(null,%s,%s,%s,%s,0,%s,%s,%s,%s,%s,%s,0,%s,sysdate())",(request.POST['atitle1'],request.POST['atitle2'],request.POST['aprice'],request.POST['aprice_old'],request.POST['adate'],request.POST['ahour'],request.POST['adetail'],request.POST['alongitude'],request.POST['alatitude'],basic_url,request.POST['pno'],))
    cursor.execute("insert into activities values(null,%s,%s,%s,%s,0,%s,%s,%s,%s,%s,%s,0,%s,sysdate())",(request.POST['atitle1'],request.POST['atitle2'],request.POST['aprice'],request.POST['aprice_old'],request.POST['adate'],request.POST['ahour'],request.POST['adetail'],request.POST['hlongitude'],request.POST['hlatitude'],basic_url,request.POST['pno'],))
    cursor.close()

    raw = {'status':1}

    resp = HttpResponse(json.dumps(raw), content_type="application/json")
    return resp

def add_city(request):

    f = request.FILES['pimg']

    root_dir = '/var/www/html/mp/static/images/citys'
    os.mkdir(root_dir)



    with open(root_dir+'/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    #pimage = request.FILES.post('pimg')

    #path = default_storage.save('static/images/'+pimage.name,ContentFile(pimage.read()))


    cursor = connections['klook'].cursor()
    cursor.execute("insert into place values(null,%s,%s,%s,%s)",(request.POST['ptitle'],'https://mina.mapglory.com/static/images/citys/'+f.name,request.POST['cityPinyin'],request.POST['cityPY'],))
    cursor.close()

    raw = {'status': 1}

    resp = HttpResponse(json.dumps(raw), content_type="application/json")
    return resp

def add_rule(request):



    cursor = connections['klook'].cursor()
    cursor.execute("insert into activity_rule values(null,%s,%s,%s)",(request.POST['rdetail'],'1',request.POST['ano']))
    cursor.close()

    raw = {'status': 1}

    resp = HttpResponse(json.dumps(raw), content_type="application/json")
    return resp

def add_ins(request):



    cursor = connections['klook'].cursor()
    cursor.execute("insert into activity_instruction values(null,%s,%s)",(request.POST['idetail'],request.POST['ano']))
    cursor.close()

    raw = {'status': 1}

    resp = HttpResponse(json.dumps(raw), content_type="application/json")
    return resp

def add_refund(request):



    cursor = connections['klook'].cursor()
    cursor.execute("insert into activity_refund_know values(null,%s,%s)",(request.POST['rdetail'],request.POST['ano']))
    cursor.close()

    raw = {'status': 1}

    resp = HttpResponse(json.dumps(raw), content_type="application/json")
    return resp

def add_use(request):


    cursor = connections['klook'].cursor()
    cursor.execute("insert into activity_use_know values(null,%s,%s,%s)",(request.POST['udetail'],request.POST['ano'],request.POST['ktype'],))
    cursor.close()

    raw = {'status': 1}

    resp = HttpResponse(json.dumps(raw), content_type="application/json")
    return resp

def add_image(request):

    ano = request.POST['ano']

    f = request.FILES['aimg']

    root_dir = '/var/www/html/mp/static/images/'+str(ano)
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)

    with open(root_dir + '/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


    cursor = connections['klook'].cursor()
    cursor.execute("insert into activity_image values(null,%s,%s)",('https://mina.mapglory.com/static/images/'+str(ano)+'/'+f.name,ano))
    cursor.close()

    if request.POST.has_key('star'):
        cursor = connections['klook'].cursor()
        cursor.execute("update activities set aurl = %s where ano = %s",('https://mina.mapglory.com/static/images/'+str(ano)+'/'+f.name,ano))
        cursor.close()

    raw = {'status': 1}

    resp = HttpResponse(json.dumps(raw), content_type="application/json")
    return resp