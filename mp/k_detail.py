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

    raw  = {}

    cursor = connections['klook'].cursor()
    cursor.execute("select * from activities where ano = %s",(ano,))
    raw['act'] = dictfetchall(cursor)
    cursor.close()

    for item in raw['act']:
        item['adate'] = json_serial(item['adate'])

    cursor = connections['klook'].cursor()
    cursor.execute("select * from activity_rule where ano = %s", (ano,))
    raw['act_rule'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select * from activity_instruction where ano = %s", (ano,))
    raw['act_ins'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select activity_package.pno,ptitle,pprice,pprice_old,rdetail from activity_package,activity_package_rule where activity_package.pno = activity_package_rule.pno and ano = %s", (ano,))
    raw['act_package'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select * from activity_order_know where ano = %s", (ano,))
    raw['act_order'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select * from activity_use_know where ano = %s", (ano,))
    raw['act_use'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select * from activity_refund_know where ano = %s", (ano,))
    raw['act_ref'] = dictfetchall(cursor)
    cursor.close()

    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response

