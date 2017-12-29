from django.http import HttpResponse

import json
from django.db import connections
from datetime import date, datetime,time


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date,time)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def dictfetchall(cursor):
	desc = cursor.description
	return [
	dict(zip([col[0] for col in desc], row))
    	for row in cursor.fetchall()
    	]

def index(request):

    openid = request.GET['openid']

    cursor = connections['default'].cursor()
    cursor.execute("select oid,orders.hno,odate,ostart,oend,orders.ocno from orders,contact,house where orders.hno = house.hno and orders.ocno = contact.cno and orders.uno = %s order by otime desc",(openid,))
    raw = dictfetchall(cursor)
    cursor.close()


    cursor = connections['default'].cursor()
    cursor.execute("select unickName,uavatarurl from Users where uid = %s",(openid,))
    uraw = dictfetchall(cursor)
    cursor.close()

    response = HttpResponse(json.dumps([raw,uraw]), content_type="application/json")
    return response