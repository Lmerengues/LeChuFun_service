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

    ano = request.GET['ano']
    raw = {}

    cursor = connections['klook'].cursor()
    cursor.execute("select pno,ptitle,pprice,pprice_old from activity_package where ano = %s", (ano,))
    raw['act_package'] = dictfetchall(cursor)
    cursor.close()

    for package in raw['act_package']:
        cursor = connections['klook'].cursor()
        cursor.execute("select rdetail from activity_package_rule where pno = %s",(package['pno'],))
        package['rule'] = dictfetchall(cursor)
        cursor.close()

    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response

def list(request):

    openid = request.GET['openid']
    raw = {}

    cursor = connections['klook'].cursor()
    cursor.execute("select unickName,uavatarurl,uscore from Users where uid = %s", (openid,))
    raw['user_info'] = dictfetchall(cursor)[0]
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select oid,otime,odate,ototal,ostatus,atitle1,aurl,tno from orders,activity_package,activities where uno = %s and orders.ano = activity_package.pno and activity_package.ano = activities.ano and ostatus > 0", (openid,))
    raw['order_info'] = dictfetchall(cursor)
    cursor.close()

    for item in raw['order_info']:
        item['odate'] = json_serial(item['odate'])
        item['otime'] = json_serial(item['otime'])
        des_str = ''
        cursor = connections['klook'].cursor()
        cursor.execute("select ttitle,pnum from order_tickets,activity_package_ticket where tid = %s and order_tickets.pno = activity_package_ticket.tno",(item['tno'],))
        arr = dictfetchall(cursor)
        for arr_item in arr:
            if int(arr_item['pnum']) != 0:
                des_str = des_str + arr_item['ttitle'] + 'x' + str(arr_item['pnum'])
        item['odes'] = des_str


    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response

def refund(request):

    oid = request.GET['oid']
    raw = {}

    cursor = connections['klook'].cursor()
    flag = cursor.execute("update orders set ostatus = 2 where oid = %s", (oid,))

    raw['status'] = flag
    cursor.close()

    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response

