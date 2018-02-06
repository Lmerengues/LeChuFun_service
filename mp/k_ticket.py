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
    cursor.execute("select * from activity_package_ticket where pno = %s",(pno,))
    raw['ticket'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select * from activity_package where pno = %s", (pno,))
    raw['package'] = dictfetchall(cursor)[0]
    cursor.close()

    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response


def create(request):

    raw  = {}
    numofticket = request.GET['numoftickets']

    cursor = connections['klook'].cursor()
    cursor.execute("select max(tid) as mtid from order_tickets where 1")
    raw['maxtid'] = int(dictfetchall(cursor)[0]['mtid'])
    cursor.close()


    mytid =  raw['maxtid']+1
    for key in numofticket:
        cursor = connections['klook'].cursor()
        cursor.execute("insert into order_tickets values(%s,%s,%s)", (str(mytid),str(key),str(numofticket[key]),))
        cursor.close()

    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response

