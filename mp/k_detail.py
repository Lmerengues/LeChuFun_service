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
    raw['act'] = dictfetchall(cursor)[0]
    raw['act']['ascore'] = (int(raw['act']['ascore'])+0.0)/10
    cursor.close()

    raw['act']['adate'] = json_serial(raw['act']['adate'])
    raw['act']['aaddtime'] = json_serial(raw['act']['aaddtime'])

    cursor = connections['klook'].cursor()
    cursor.execute("select rno,rdetail,activity_rule.rno,iurl from activity_rule,icon where activity_rule.ino = icon.ino and ano = %s", (ano,))
    raw['act_rule'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select * from activity_instruction where ano = %s", (ano,))
    raw['act_ins'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select pno,ptitle,pprice,pprice_old from activity_package where ano = %s", (ano,))
    raw['act_package'] = dictfetchall(cursor)
    cursor.close()

    for package in raw['act_package']:
        cursor = connections['klook'].cursor()
        cursor.execute("select rdetail from activity_package_rule where pno = %s",(package['pno'],))
        package['rule'] = dictfetchall(cursor)
        cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select * from activity_order_know where ano = %s and ktype = 1", (ano,))
    raw['act_order_1'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select * from activity_order_know where ano = %s and ktype = 2", (ano,))
    raw['act_order_2'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select * from activity_use_know where ano = %s and ktype = 0", (ano,))
    raw['act_use_0'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select * from activity_use_know where ano = %s and ktype = 1", (ano,))
    raw['act_use_1'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select * from activity_use_know where ano = %s and ktype = 2", (ano,))
    raw['act_use_2'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select * from activity_refund_know where ano = %s", (ano,))
    raw['act_ref'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select * from activity_use_know where ano = %s and ktype = 0", (ano,))
    raw['act_use_0'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select uno,cdetail,cscore,cdate,unickName,uavatarurl from activity_comment,Users where activity_comment.uno = Users.uid and ano = %s order by cdate desc limit 1", (ano,))
    raw['comment'] = dictfetchall(cursor)[0]
    raw['comment']['cdate'] = json_serial(raw['comment']['cdate'])
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute("select count(*) as cou from activity_comment where ano = %s",(ano,))
    raw['comment_num'] = dictfetchall(cursor)[0]
    cursor.close()



    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response

def comment(request):
    ano = request.GET['ano']

    raw = {}
    cursor = connections['klook'].cursor()
    cursor.execute("select uno,cdetail,cscore,cdate,unickName,uavatarurl from activity_comment,Users where activity_comment.uno = Users.uid and ano = %s order by cdate desc",(ano,))

    raw['comment'] = dictfetchall(cursor)

    for comment in raw['comment']:
        comment['cdate'] = json_serial(comment['cdate'])

    cursor.close()

    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response