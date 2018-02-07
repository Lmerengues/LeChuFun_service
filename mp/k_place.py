from django.http import HttpResponse

import json
from django.db import connections

from datetime import date, datetime,time

import math

def dictfetchall(cursor):
	desc = cursor.description
	return [
	dict(zip([col[0] for col in desc], row))
    	for row in cursor.fetchall()
    	]

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date,date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def index(request):

    raw = {}

    cursor = connections['klook'].cursor()
    cursor.execute(
        "select place_hot.pno as pid,ptitle,purl from place,place_hot where place.pno = place_hot.pno order by pval desc")
    raw['hot_place'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select ptitle as cityName,cityPinYin,cityPY,pno from place order by cityPY")
    raw['citys'] = dictfetchall(cursor)
    cursor.close()

    response=HttpResponse(json.dumps(raw), content_type="application/json")
    return response

def detail(request):

    raw = {}
    pno = request.GET['pno']

    cursor = connections['klook'].cursor()
    cursor.execute("select purl from place where pno = %s",(request.GET['pno'],))
    raw['purl'] = dictfetchall(cursor)[0]['purl']
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select ano,atitle1,anum,ascore,aprice,aprice_old,ahour,adate,aurl,ptitle from activities,place where activities.pno = %s and activities.pno = place.pno order by anum desc limit 10",(pno,))
    raw['hot_acti'] = dictfetchall(cursor)
    cursor.close()

    for item in raw['hot_acti']:
        item['adate'] = json_serial(item['adate'])

    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response

