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
        "select * from base")
    raw['base'] = dictfetchall(cursor)[0]
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute(
        "select place_hot.pno,ptitle,purl from place,place_hot where place.pno = place_hot.pno order by pval desc")
    raw['hot_place'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute(
        "select activity_rank_hot.ano,atitle1,anum,ascore,aprice,aprice_old,ahour,adate,aurl,ptitle from activities,activity_rank_hot,place where activities.ano = activity_rank_hot.ano and activities.pno = place.pno order by aval desc limit 5")
    raw['hot_acti'] = dictfetchall(cursor)
    cursor.close()

    for item in raw['hot_acti']:
        item['adate'] = json_serial(item['adate'])

    cursor = connections['klook'].cursor()
    cursor.execute(
        "select activity_rank_theme.ano,atitle1,anum,ascore,aprice,aprice_old,ahour,adate,aurl,ptitle from activities,activity_rank_theme,place where activities.ano = activity_rank_theme.ano and activities.pno = place.pno order by aval desc limit 5")
    raw['theme_acti'] = dictfetchall(cursor)
    cursor.close()

    for item in raw['theme_acti']:
        item['adate'] = json_serial(item['adate'])

    cursor = connections['klook'].cursor()
    cursor.execute(
        "select activity_rank_recommend.ano,atitle1,anum,ascore,aprice,aprice_old,ahour,adate,aurl,ptitle from activities,activity_rank_recommend,place where activities.ano = activity_rank_recommend.ano and activities.pno = place.pno order by aval desc limit 5")
    raw['rec_acti'] = dictfetchall(cursor)
    cursor.close()


    for item in raw['rec_acti']:
        item['adate'] = json_serial(item['adate'])

    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response
