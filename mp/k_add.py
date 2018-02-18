from django.http import HttpResponse

import json
from django.db import connections

from datetime import date, datetime,time

import math
import os

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


    pimage = request.FILES.post('pimg')
    baseDir = os.path.dirname(os.path.abspath(__name__))
    jpgdir = os.path.join(baseDir, 'static', 'images')
    filename = os.path.join(jpgdir, pimage.name)
    fobj = open(filename, 'wb')
    for chrunk in pimage.chunks():
        fobj.write(chrunk)
    fobj.close()


    cursor = connections['klook'].cursor()
    cursor.execute("insert into place values(null,%s,%s,%s,%s)",(request.POST['ptitle'],'aa',request.POST['cityPinyin'],request.POST['cityPY'],))
    cursor.close()

    raw = {'status': 1}

    resp = HttpResponse(json.dumps(raw), content_type="application/json")
    return resp

