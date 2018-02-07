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
    pno = request.GET['pno']

    raw = {}

    cursor = connections['klook'].cursor()
    cursor.execute("select activities.ano,atitle1,anum,ascore,aprice,aprice_old,ahour,adate,aurl,ptitle from activities,place,activity_type where activities.pno = %s and activities.pno = place.pno and activities.ano = activity_type.ano and tno = 2 order by anum desc",(pno,))
    raw['list'] = dictfetchall(cursor)
    cursor.close()

    for item in raw['list']:
        item['adate'] = json_serial(item['adate'])

    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response