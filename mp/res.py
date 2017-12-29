from django.http import HttpResponse

import json
from django.db import connections

def dictfetchall(cursor):
	desc = cursor.description
	return [
	dict(zip([col[0] for col in desc], row))
    	for row in cursor.fetchall()
    	]

def index(request):

    openid = request.GET['openid']

    cursor = connections['default'].cursor()
    cursor.execute("select oid,orders.hno,odate,ostart,oend,orders.ocno from orders,contact,house"
                   "where orders.hno = house.hno and orders.ocno = contact.cno and orders.uno = %s order by orders.otime desc",(openid,))
    raw = dictfetchall(cursor)
    cursor.close()

    cursor = connections['default'].cursor()
    cursor.execute("select unickName,uavatarurl from Users where uid = %s",(openid,))
    uraw = dictfetchall(cursor)
    cursor.close()

    response = HttpResponse(json.dumps([raw,uraw]), content_type="application/json")
    return response