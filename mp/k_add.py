from django.http import HttpResponse

import json
from django.db import connections

from datetime import date, datetime,time

import math

def add_activity(request):

    basic_url = 'https://mina.mapglory.com/static/images/canaan/5.jpeg'

    cursor = connections['klook'].cursor()
    #cursor.execute("insert into activities values(null,%s,%s,%s,%s,0,%s,%s,%s,%s,%s,%s,0,%s,sysdate())",(request.POST['atitle1'],request.POST['atitle2'],request.POST['aprice'],request.POST['aprice_old'],request.POST['adate'],request.POST['ahour'],request.POST['adetail'],request.POST['alongitude'],request.POST['alatitude'],basic_url,request.POST['pno'],))
    cursor.execute("insert into activities values(null,%s,%s,%s,%s,0,%s,%s,%s,%s,%s,'asd',0,'0',sysdate())",(request.POST['atitle1'],request.POST['atitle2'],request.POST['aprice'],request.POST['aprice_old'],request.POST['adate'],request.POST['ahour'],request.POST['adetail'],request.POST['hlongitude'],request.POST['hlatitude'],))
    cursor.close()

    raw = {'status':1}

    resp = HttpResponse(json.dumps(raw), content_type="application/json")
    return resp

