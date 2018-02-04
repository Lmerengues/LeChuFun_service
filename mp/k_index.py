from django.http import HttpResponse

import json
from django.db import connections

import math

def dictfetchall(cursor):
	desc = cursor.description
	return [
	dict(zip([col[0] for col in desc], row))
    	for row in cursor.fetchall()
    	]


def index(request):

    raw = {}
    cursor = connections['klook'].cursor()
    cursor.execute(
        "select place_hot.pno,ptitle,purl from place,place_hot where place.pno = place_hot.pno order by pval desc")
    raw['hot_place'] = dictfetchall(cursor)
    cursor.close()

    cursor = connections['klook'].cursor()
    cursor.execute(
        "select activity_rank_hot.ano,atitle1,anum,ascore,aprice,aprice_old,ahour,aurl from activities,activity_rank_hot where activities.ano = activity_rank_hot.ano order by aval desc")
    raw['hot_acti'] = dictfetchall(cursor)
    cursor.close()





    response = HttpResponse(json.dumps(raw), content_type="application/json")
    return response